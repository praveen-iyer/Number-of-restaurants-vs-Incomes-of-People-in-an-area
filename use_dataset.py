import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import sys
from get_dataset import *

# Function to perform simple linear regression for each predictor
def simpleLinearRegression(x, y, feat,plot = True):
	
	trainX = sm.add_constant(x, prepend=False)
	olsres = sm.OLS(y, trainX).fit()
	
	print("For",feat,"\n",olsres.summary())

	if plot:
		fname = "{}_plot.png".format(feat)
		fig, ax = plt.subplots(figsize=(12, 7))
		with plt.style.context('ggplot'):
			ax.scatter(x, y, alpha=0.3, label="Samples")
			ax.plot(x, olsres.predict(trainX), "tab:red", alpha=0.8, label="Linear Rgression Hypothesis")
		ax.set_title("Simple Linear Regression for {}".format(feat))
		ax.set_xlabel(feat)
		ax.set_ylabel("Number of restaurants")
		ax.legend()
		plt.savefig(fname)
		plt.show()

	return olsres

def perform_analysis(df):
	df_allX = df.iloc[:,:-1]
	df_Y = df.iloc[:,-1]
	feats = []
	for i,feat in enumerate(df_allX.columns):
		var_name = "df_"+feat
		feats.append(feat)
		exec(var_name+"=df_allX.iloc[:,i]")
	# feats.append("allX")
	print("Feats:",feats)

	for feat in feats:
		x_feat = "df_"+feat
		model_name = "model_"+feat
		print("\n\n-----------------------------For {}-----------------------------\n\n".format(feat))
		exec("{} = simpleLinearRegression({},df_Y,feat)".format(model_name,x_feat))

	print("\n\n-----------------------------For All features-----------------------------\n\n")
	exec("{} = simpleLinearRegression({},df_Y,'All features' ,plot=False)".format("model_allX","df_allX"))

	print("\n\n")
	s = '''
	Since for all features the p-value based on the null hypothesis testing is greater than 0.05 
	we can conclude that the features do not affect the number of restaurants based on the distribution 
	we have. Hence no model to predict the number of restaurants has been made.'''
	print(s)
	print("\n\n")

if __name__ == '__main__':
	l = sys.argv
	if len(l)==1: # Assemble and make the complete dataset and then perform analysis on the dataset
		zips = get_inhabited_zip_codes_in_LA()
		print("Number of zip codes is",len(zips))
		df = get_dataset(zips)
		perform_analysis(df)

	elif len(l)==3 and l[1]=='--static': # Perform analysis on the already existing CSV file
		path = l[2]
		df = pd.read_csv(path,index_col=0)
		perform_analysis(df)

	else: # Print a statement for the wrong/unrecognized arguments input
		print("The arguments do not match the requirements. Please refer README.md for understanding the requirements")