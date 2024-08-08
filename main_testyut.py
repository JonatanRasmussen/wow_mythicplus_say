from src.format_spelllist import FormatSpelllist
#%%
if __name__ == "__main__":
    df = FormatSpelllist.load_encounters_df()
    FormatSpelllist.main(df)

