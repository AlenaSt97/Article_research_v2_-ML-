# Article_research_v2_-ML-
This project is devoted to the analysis of scientific articles on the topic of the main types of blood cells. I'm trying to determine what type of cell the article is about using machine learning and information about the cell markers mentioned in the article.

The process consists of two stages:
At the first step, the data is automatically collected by **parser.py** into the database **cell_markers.sqlite**. For each of the main types of blood cells (monocytes, T-lymphocytes, B-lymphocytes, NK-lymphocytes, neutrophils, eosinophils, basophils, macrophages, erythrocytes and platelets), I took about 100 articles per type for analysis (that is, about 1000 articles in total). I counted the mention in the article of all cell markers and cell names from this list.

At the second step, I analyze the received data and train the classification model.
First of all, I removed insignificant samples and markers, chose a method for preprocessing: for a table with markers, I chose MaxAbsScaler, since the data in it turned out to be sparse, for a table with cell names - Normalizer and Binarizer for an unambiguous choice of the prevailing class.
Then I tested 3 classifiers: LogisticRegressionCV, MultinomialNB and LinearSVC to find out which one is best for solving the classification problem on my data. All three classifiers showed approximately the same precision score - about 0.75

And finally, I'm trying to figure out how to further improve this model.

More detailed description of the work process you can see in the **data_processing.ipynb file**.
