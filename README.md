# DataScience-learning
>My course work for the Applied Data Science with Python in Coursera

## Course 1: Introduction to Data Science in Python
### Week 1: Python Fundamentals
* basic Python functions, types, strings and dates
* read and write csv files
* map, lambda, list
* numpy

### Week 2: Basic Data Processing with Pandas
* data structure: series and dataframe
* dataframe manipulation: loading, indexing, querying and dealing with missing values
* assignment reflections: 
	* sort the value of the dictionary: turn the dictionary into a tuple (use .items()), then use sorted() to sort the values in the tuple
	* different ways of indexing: df['column_name'] get a column, df.loc['index_name'] get a row, df.iloc[a,b] get the value of a cell
	
### Week 3: Advanced Pandas
* merge, group by and scale the data
* pivot tables and date functions
* assignment reflections: 
	* excute function by row: df.apply(function, axis=1)
	* scale the data: cut() + Categorical()
	* convert a float number to a string with thousands separator: format(number,',')
	
### Week 4: Statistical Analysis
* distributions and hypothesis testing
* assignment reflections: 
	* change the name of a column: use .T to transpose the dataframe, then use .rename() to change the name by row
	* change a dataframe to a tuple: tuple(x) for x in df.values
	* get the data which is not from tuple_list from a dataframe: df.loc[~df.index.isin(tuple_list)].dropna()
	
### Course reflections:
* data pre-pocessing is extremely important, because if not handled properly, the rest of the work will be no sense
* pandas is a powerful tool which can handle complex problems with one line of code
* multiple check is necessary when doing the data analysis project, small mistakes may totally change the outcome

