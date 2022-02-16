# anti-corruption-bot

Test API (running via Flask) is currently hosted at https://uk-mp-voting-data-test1.herokuapp.com/ (to be eventually migrated to AWS Lambda)
 
**Available endpoints:**
- *get_mp_list* - Returns a list of all active MPs
- *get_mp_votes* - Returns a list of voting positions for a specific MP (must provide a **personId** in the query)
- *get_mp_name* - Returns an MP name (based on the provided **personId**)
- *get_mp_data* - Returns an MP's full metadata (based on the provided **personId**)
- *get_mp_data_by_name* - Returns an MP's full metadata (based on the provided **name**)
- *get_mp_votes_by_name* - Returns a list of voting positions for a specific MP (must provide a **name** in the query)

e.g. https://uk-mp-voting-data-test1.herokuapp.com/get_mp_name?personId=10001
e.g. https://uk-mp-voting-data-test1.herokuapp.com/get_mp_votes_by_name?name=Keir%20Starmer
