# mcnulty

My current plan is to predict the type of cuisine in a restaurant based on menu items on their menu.

I found a dataset of historic menus from the New York Public Library (http://menus.nypl.org/data). It seems like there may be some interesting information there, however one key piece of information that seems to be missing is the type of cuisine that is featured at the restaurant. I did think it would may be useful to be able to predict the type of restaurant based on menu items in order to supplement this dataset with type of cuisine.

It could also be useful for websites that specialize in providing ordering and delivery services for multiple different types of restaurants (UberEats, GrubHub, Caviar, etc.) to better categorize the restaurants on their website in order to make sure they are providing accurate information to the consumer.

I have currently found the EatStreet API (https://developers.eatstreet.com/) that allows me to do searches in different cities around the country in order to find online restaurants with links to menus. I've currently used the latitutde and longitude of the 1000 largest cities in the US to do queries within a 25 mile radius of each city and to get all the restaurants that allow for pickup and delivery in that radius. This provided me with around 110,000 restaurants (although there is likely to be some duplication if cities are close to each other like Oakland and San Francisco, so there will need to be some filtering for duplicates) where I am working on getting all the menu items at each of them.

I know I may have to do some NLP or just finding the keywords from the menu items, but I've currently obtained about 20,000 menus from the restaurants that will allow me to start looking at the keywords on menus. The size of both the restaurant database and menu database definitely lends itself to the use of SQL.

