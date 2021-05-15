# For 1.0.0 release:

- **COMPLETE** Sort Gen med for both lists
- Better documentation
  - Setup / install process
  - Usage instructions on main page
  - Documentation of development / deployment configuration
- Better centering for time clock
- Actual setup scripts
- Interface for modifying callback numbers
- Split into separate python scripts
- Calculate best-estimate of elapsed-time for signouts
- From B.C.: - Notification messages after 7:15 not 7:30
- From B.C.: More predictable refresh (every 1 min?  save form data?  not within 30s of submit time? more freq for NF page?)
- From B.C.: Don't notify on Gen med non-signouts. 
- From S.N.: Put gen med at the bottom of the signout form so that it isn't accidentally selected.

# Post v0.4 upgrade

- **COMPLETE** Nightfloat page should not refresh when an active signout is in progress (061b269c17fb9444c671ef6c3fa7dd923a5392ee)
- **COMPLETE** There is no Lymphoma #3. There is a Lymphoma green APP.
- **COMPLETE** Add note to the 'add page' demonstrating the normal formatting of the list names (6ad8ec64dbf96291346596b80093fa3387622429)
- ? Add ability for NF to 'add lists' to the person currently signing out
- **WILL NOT DO: better to use the arcane curl syntax on the CLI** Web interface for changing configuration values
- **COMPLETE** Fix for the insertContact not putting in the right email address on some pages (ex: submission, works fine on query) (aaa4519eaf660d1adfcf2c69a6afaeb34deac75c)
- **COMPLETE** UI and logging cleanup (2acc089a9bca2156b55abfc572cb0e4ae3aac62c)
- **COMPLETE WITH MODS: Uses curl on CLI*** Web interface for interrogating server state
- **COMPLETE** Admin interface for changing service lists: (3a21e20102042741c27116403a3e0be60fa6f3b5)
- **COMPLETE** Millisecond timing for system clock sync (75fb038334290b13b34d6a2963d07e5d76e6195e)

# TODO for v0.3 release

- **COMPLETE** - Put Gen Med to the top of every sign out list (b13a23197b3aa8e777bd150cbb48cc76eb9bacfbdd)
- **COMPLETE** Add precision to the clock at top of submission page and resync/reload page regularly (75fb038334290b13b34d6a2963d07e5d76e6195e)
- **COMPLETE** Add precision to query page (3fc99ecef7fb82c074326b62047f81fe54c0020e)
- **COMPLETE** Display callbacks before and after calls (13969656f53df0f1ec666d175139cce0e20dbed9)
- **COMPLETE** Add email address to send problems/ bug reports to (44ffc826a31addd8c945d203e7449b45bf7d4d2b)
- **COMPLETE** NEW - Send a Text message to NF if someone adds their name to a list after it is already 'empty' (8c86ee4361d10b743e06436b3c735ba93d42f396)
- **COMPLETE** Cron script using twilio to text night float if signout not received for a list by 9pm
  - **COMPLETE** Database for NF and callback numbers (db4c24b2ecea222b3332459ae3d7067a838d89a7)
  - **COMPLETE** Identify callbacks that have/haven't happened (df1f3c1009302e0a8a4ea430d59925cdae042660)
  - **COMPLETE** Ability to send texts based on DB search (d10241c35aceaced824e6576bdd5fa25a1a873ba)
  - **COMPLETE** Working testable cron job (2861ee99ab89aafab72efbffaec7a3b4795163a8)
  - Test deployment
  - Finalizd
- **COMPLETE** FIX for messed up `fix_timestamps` function in main python file for :59:59 times (ffceccc0ce62ab45353930b3c304674309ae27eb)
- **COMPLETE** Switch to using active field for displaying choices in submission page (d469673051ccb55e4e8664096cc0fe00808b61c7)
- **COMPLETE** Set unused entries to not show as active (Leukemia A/B, STR NPs, GI C and GI D) (d469673051ccb55e4e8664096cc0fe00808b61c7)
  - Requires running `scripts/updatedb.sh scripts/fix_service_active.sql`
- **COMPLETE** Warn that best if using chrome (d469673051ccb55e4e8664096cc0fe00808b61c7)
- **COMPLETE** Have javascript re-sync time every 15 seconds (to work around bug in IE) (75fb038334290b13b34d6a2963d07e5d76e6195e)
- **COMPLETE** Multi-signout for weekdays as well (3a21e20102042741c27116403a3e0be60fa6f3b5)
- **PARTIAL** Timed auto-refresh of submission and nightfloat callback pages (3a21e20102042741c27116403a3e0be60fa6f3b5)
  - **COMPLETE** Nightfloat page will auto-refresh every 60 seconds to ensure that newly added
  - Not needed - refreshing submission page

# COMPLETED tasks

- Only 1 list per NF on weekends **COMPLETE**
- More accurate time representation **COMPLETE**
- Start and stop buttons **COMPLETE**
- Multi-select for weekends **COMPLETE**
- Melodik the Ref sheets **COMPLETE**
- Instructions for late sign ups **COMPLETE**
- Fix to never display "too early" signouts **COMPLETE**
