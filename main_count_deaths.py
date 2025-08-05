import csv
import ast
import datetime
from collections import Counter
import pandas as pd
from typing import List, Union
from src.class_wowhead_spell import WowheadSpell
from src.config.consts_file_paths import FilePathConsts
from src.config.global_configs import GlobalConfigs

def format_seconds_to_hms(seconds: Union[int, float, None]) -> str:
    """Converts seconds into HH:MM:SS format."""
    if seconds is None or not isinstance(seconds, (int, float)) or seconds < 0:
        return "N/A"
    return str(datetime.timedelta(seconds=int(seconds)))

def analyze_deadly_spells_per_boss(csv_filepath, output_filepath="deadly_spells_analysis.txt", top_n=10):
    # Main data structure for initial data collection
    analysis_data = {}
    all_spell_ids = set()

    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                boss_name = row.get('fight_boss_text')
                deaths_str = row.get('ally_deaths')
                setup_level_str = row.get('setup_level')
                ability_list_str = row.get('ability_list')
                fight_outcome = row.get('fight_outcome')
                fight_duration_sec_str = row.get('fight_duration_in_sec')

                if not boss_name or not setup_level_str or not fight_outcome:
                    continue

                if fight_outcome not in ['kill', 'wipe']:
                    continue

                try:
                    setup_level = int(float(setup_level_str))
                except (ValueError, TypeError):
                    continue

                level_category = "high_level" if setup_level >= 16 else "mid_level" if 10 <= setup_level <= 15 else None
                if level_category is None:
                    continue

                if boss_name not in analysis_data:
                    analysis_data[boss_name] = {}
                if level_category not in analysis_data[boss_name]:
                    analysis_data[boss_name][level_category] = {}
                if fight_outcome not in analysis_data[boss_name][level_category]:
                    analysis_data[boss_name][level_category][fight_outcome] = {
                        "sample_size": 0,
                        "killing_blows": Counter(),
                        "spell_names": {},
                        "total_duration_sec": 0,
                    }

                data_bucket = analysis_data[boss_name][level_category][fight_outcome]
                data_bucket['sample_size'] += 1

                # If the run was a kill, add its duration for averaging
                if fight_outcome == 'kill' and fight_duration_sec_str:
                    try:
                        duration_sec = int(fight_duration_sec_str)
                        data_bucket['total_duration_sec'] += duration_sec
                    except (ValueError, TypeError):
                        pass  # Ignore if duration is not a valid number

                if ability_list_str and ability_list_str != '[]':
                    try:
                        ability_events = ast.literal_eval(ability_list_str)
                        for event_string in ability_events:
                            parts = event_string.split('░')
                            if len(parts) == 3 and parts[0].isnumeric():
                                spell_id, spell_name = parts[0], parts[1]
                                all_spell_ids.add(spell_id)
                                if spell_id not in data_bucket['spell_names']:
                                    data_bucket['spell_names'][spell_id] = spell_name
                    except (ValueError, SyntaxError):
                        pass

                if deaths_str and deaths_str != '[]':
                    try:
                        death_events = ast.literal_eval(deaths_str)
                        for event_string in death_events:
                            parts = event_string.split('░')
                            if len(parts) > 2 and parts[2].isnumeric():
                                kb_name, kb_id = parts[1], parts[2]
                                data_bucket['killing_blows'][kb_id] += 1
                                all_spell_ids.add(kb_id)
                                if kb_id not in data_bucket['spell_names']:
                                    data_bucket['spell_names'][kb_id] = kb_name
                    except (ValueError, SyntaxError):
                        continue
    except Exception as e:
        print(f"An unexpected error occurred during data processing: {e}")
        return

    # This section for fetching Wowhead data remains unchanged
    print(f"Total unique spell IDs: {len(all_spell_ids)}")
    print("\nCreating wowhead spell_id csv of all Unique Spell IDs found in CSV:")
    i = 0
    wowhead_spells = [WowheadSpell(spell_id) for spell_id in all_spell_ids]
    # Simulating the progress printout
    for i, _ in enumerate(wowhead_spells, 1):
        if i == 1 or i % 50 == 0 or i == len(wowhead_spells):
            print(f"{i} of {len(wowhead_spells)}")

    df_wowhead_spells = WowheadSpell.write_wowhead_spell_ids_to_csv(wowhead_spells)

    spell_info_map = {}
    spell_name_to_npc_map = {}
    for _, row in df_wowhead_spells.iterrows():
        spell_id_str = str(row['spell_id'])
        spell_info_map[spell_id_str] = {'npc_id': row['npc_id'], 'npc_name': row['npc_name']}
        if WowheadSpell.is_valid_npc(row['npc_name'], row['npc_id']) and row['spell_name'] not in spell_name_to_npc_map:
            spell_name_to_npc_map[row['spell_name']] = {'npc_id': row['npc_id'], 'npc_name': row['npc_name']}

    if not analysis_data:
        print("No valid data found to analyze.")
        return

    print(f"Generating analysis report to '{output_filepath}' and console...")

    with open(output_filepath, mode='w', encoding='utf-8') as outfile:
        def write_report(line=""):
            print(line)
            outfile.write(line + '\n')

        for boss_name, categories in sorted(analysis_data.items()):
            mid_kill_data = categories.get('mid_level', {}).get('kill', {})
            high_kill_data = categories.get('high_level', {}).get('kill', {})
            mid_wipe_data = categories.get('mid_level', {}).get('wipe', {})
            high_wipe_data = categories.get('high_level', {}).get('wipe', {})

            # --- AVERAGE DURATION CALCULATION ---
            ss_mk_kill = mid_kill_data.get('sample_size', 0)
            dur_mk_kill = mid_kill_data.get('total_duration_sec', 0)
            avg_dur_mk = dur_mk_kill / ss_mk_kill if ss_mk_kill > 0 else None

            ss_hk_kill = high_kill_data.get('sample_size', 0)
            dur_hk_kill = high_kill_data.get('total_duration_sec', 0)
            avg_dur_hk = dur_hk_kill / ss_hk_kill if ss_hk_kill > 0 else None

            total_ss_kill = ss_mk_kill + ss_hk_kill
            total_dur_kill = dur_mk_kill + dur_hk_kill
            avg_dur_total = total_dur_kill / total_ss_kill if total_ss_kill > 0 else None

            avg_time_str = (f"Avg. Time (All): {format_seconds_to_hms(avg_dur_total)} | "
                            f"Avg. Time (<15): {format_seconds_to_hms(avg_dur_mk)} | "
                            f"Avg. Time (16+): {format_seconds_to_hms(avg_dur_hk)}")

            def get_dpr_stats(data_bucket, spell_id):
                sample_size = data_bucket.get('sample_size', 0)
                if sample_size == 0:
                    return "N/A"
                kb_count = data_bucket.get('killing_blows', {}).get(spell_id, 0)
                return (kb_count / sample_size) * 100

            all_boss_spell_ids = set()
            all_data_buckets = [mid_kill_data, high_kill_data, mid_wipe_data, high_wipe_data]
            for data in all_data_buckets:
                all_boss_spell_ids.update(data.get('spell_names', {}).keys())
                all_boss_spell_ids.update(data.get('killing_blows', {}).keys())

            final_stats_list = []
            for spell_id in all_boss_spell_ids:
                spell_name = next((d.get('spell_names', {}).get(spell_id) for d in all_data_buckets if d.get('spell_names', {}).get(spell_id)), "Unknown")

                dpr_mk = get_dpr_stats(mid_kill_data, spell_id)
                dpr_hk = get_dpr_stats(high_kill_data, spell_id)
                dpr_mw = get_dpr_stats(mid_wipe_data, spell_id)
                dpr_hw = get_dpr_stats(high_wipe_data, spell_id)

                final_stats_list.append({
                    'id': spell_id,
                    'name': spell_name,
                    'dpr_mid_kill': dpr_mk if isinstance(dpr_mk, float) else -1.0,
                    'd_mid_kill': mid_kill_data.get('killing_blows', {}).get(spell_id, 0),
                    'dpr_high_kill': dpr_hk if isinstance(dpr_hk, float) else -1.0,
                    'd_high_kill': high_kill_data.get('killing_blows', {}).get(spell_id, 0),
                    'dpr_mid_wipe': dpr_mw if isinstance(dpr_mw, float) else -1.0,
                    'd_mid_wipe': mid_wipe_data.get('killing_blows', {}).get(spell_id, 0),
                    'dpr_high_wipe': dpr_hw if isinstance(dpr_hw, float) else -1.0,
                    'd_high_wipe': high_wipe_data.get('killing_blows', {}).get(spell_id, 0),
                })

            sorted_stats = sorted(final_stats_list, key=lambda x: x['dpr_mid_kill'], reverse=True)

            ss_mk = mid_kill_data.get('sample_size', 0)
            ss_hk = high_kill_data.get('sample_size', 0)
            ss_mw = mid_wipe_data.get('sample_size', 0)
            ss_hw = high_wipe_data.get('sample_size', 0)

            header_mk = f"FULLRUN(<15) (N={ss_mk})"
            header_hk = f"FULLRUN(16+) (N={ss_hk})"
            header_mw = f"DISBAND(<15) (N={ss_mw})"
            header_hw = f"DISBAND(16+) (N={ss_hw})"

            write_report("\n" + "="*144)
            write_report(f" BOSS ENCOUNTER ANALYSIS: {boss_name} ({ss_mk+ss_hk+ss_mw+ss_hw} runs)")
            write_report(avg_time_str) # ADDED LINE
            write_report("="*144)
            write_report(f"\n--- Top {top_n} Most Deadly Spells (Deaths per Run) ---")
            write_report("Ranked by Deaths/Run for Full Clears in Levels 10-15.")
            write_report("-" * 144)

            header = (f"{'Rank':<5} | {'Spell Name':<20} | {'NPC Name':<20} | "
                      f"{header_mk:<20} | {header_hk:<20} | {header_mw:<20} | {header_hw:<20}")
            write_report(header)
            write_report("-" * 144)

            for i, stats in enumerate(sorted_stats[:top_n], 1):
                rank = f"{i}."
                spell_id = stats['id']
                spell_name_from_log = stats['name']

                dpr_mk_str = f"{stats['dpr_mid_kill']:.1f}%" if stats['dpr_mid_kill'] >= 0 else "N/A"
                dpr_hk_str = f"{stats['dpr_high_kill']:.1f}%" if stats['dpr_high_kill'] >= 0 else "N/A"
                dpr_mw_str = f"{stats['dpr_mid_wipe']:.1f}%" if stats['dpr_mid_wipe'] >= 0 else "N/A"
                dpr_hw_str = f"{stats['dpr_high_wipe']:.1f}%" if stats['dpr_high_wipe'] >= 0 else "N/A"

                npc_name_str = "N/A"
                if spell_id in spell_info_map:
                    npc_info = spell_info_map[spell_id]
                    if WowheadSpell.is_valid_npc(npc_info['npc_name'], npc_info['npc_id']):
                        npc_name_str = npc_info['npc_name']
                    elif spell_name_from_log in spell_name_to_npc_map:
                        npc_name_str = spell_name_to_npc_map[spell_name_from_log]['npc_name']

                spell_name_display = (spell_name_from_log[:18] + '..') if len(spell_name_from_log) > 20 else spell_name_from_log
                npc_name_display = (npc_name_str[:18] + '..') if len(npc_name_str) > 20 else npc_name_str

                row_str = (f"{rank:<5} | {spell_name_display:<20} | {npc_name_display:<20} | "
                           f"{dpr_mk_str:<20} | {dpr_hk_str:<20} | {dpr_mw_str:<20} | {dpr_hw_str:<20}")
                write_report(row_str)

    print(f"\nAnalysis complete. Report saved to '{output_filepath}'.")

if __name__ == "__main__":
    csv_path = FilePathConsts.wcl_log_encounter_csv_path(GlobalConfigs.WCL_ZONE_ID)
    analyze_deadly_spells_per_boss(csv_path, top_n=50)