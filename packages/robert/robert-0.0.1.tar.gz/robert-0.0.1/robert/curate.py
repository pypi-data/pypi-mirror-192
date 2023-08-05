"""
Parameters
----------

	 csv_name : str, default=''
		 Name of the CSV file. A path can be provided (i.e. 'C:/Users/FOLDER/FILE.csv'). 
	 y : str, default=''
		 Name of the column containing the response variable in the input CSV file (i.e. 'solubility'). 
	 discard : list, default=[]
		 List containing the columns of the input CSV file that will not be included as descriptors
		 (i.e. ['name','SMILES']). The y value is automatically excluded.
	 categorical : str, default='onehot'
		 Mode to convert data from columns with categorical variables. As a example, a variable containing 4
		 types of C atoms (i.e. primary, secondary, tertiary, quaternary) will be converted into categorical
		 variables. Options: 'onehot' (for one-hot encoding, ROBERT will create a descriptor for each type of
		 C atom using 0s and 1s to indicate whether the C type is present), 'numbers' (to describe the C atoms
		 with numbers: 1, 2, 3, 4).
	 corr_filter : bool, default=True
		 Activate the correlation filters of descriptors. Two filters will be performed based on the correlation
		 of the descriptors with other descriptors (x filter) and the y values (y filter).
	 thres_x : float, default=0.85
		 Thresolhold to discard descriptors based on high R**2 correlation with other descriptors (i.e. 
		 if thres_x=0.85, variables that show R**2 > 0.85 will be discarded).
	 thres_y : float, default=0.02
		 Thresolhold to discard descriptors with poor correlation with the y values based on R**2 (i.e.
		 if thres_y=0.02, variables that show R**2 < 0.02 will be discarded).
	 destination : str, default=None,
		 Directory to create the output file(s)  

"""
#####################################################.
#         This file stores the CURATE class         #
#               used in data curation               #
#####################################################.

import os
import sys
import time
import pandas as pd
from scipy import stats
from robert.utils import load_variables


class curate:
	"""
	Class containing all the functions from the CURATE module.

	Parameters
	----------
	kwargs : argument class
		Specify any arguments from the CURATE module (for a complete list of variables, visit the ROBERT documentation)
	"""

	def __init__(self, **kwargs):

		start_time_overall = time.time()

		# load default and user-specified variables
		self.args = load_variables(kwargs, "curate")

		# initial sanity checks
		self.sanity_checks('initial', None)

		# load database
		csv_df = pd.read_csv(self.args.csv_name+'.csv')
		self.sanity_checks('csv_db',csv_df.columns)
		csv_df = csv_df.drop(self.args.discard, axis=1)

		self.args.log.write(f'\no  Database {self.args.csv_name} loaded successfully, including:')
		self.args.log.write(f'\n   {len(csv_df[self.args.y])} datapoints')
		self.args.log.write(f'\n   {csv_df.columns} descriptors (excluding the {len(self.args.discard)} descriptors from the discard option)')

		# transform categorical descriptors
		csv_df = self.categorical_transform(csv_df)

		# applies the correlation filters and returns the database without correlated descriptors
		if self.args.corr_filter:
			csv_df = self.correlation_filter(csv_df)
				
		elapsed_time = round(time.time() - start_time_overall, 2)
		self.args.log.write(f"\nTime CURATE: {elapsed_time} seconds\n")
		self.args.log.finalize()

		# this is added to avoid path problems in jupyter notebooks
		os.chdir(self.args.initial_dir)


	def sanity_checks(self, type_checks, columns_csv):
		"""
		Check that different variables are set correctly
		"""

		curate_valid = True
		if type_checks == 'initial':
			if self.args.csv_name is '':
				self.args.log.write('\nx  Specify the name of your CSV file with the csv_name option!')
				curate_valid = False

			elif not os.path.exists(self.args.csv_name):
				self.args.log.write(f'\nx  The path of your CSV file doesn\'t exist! You specified: {self.args.csv_name}')
				curate_valid = False

			elif self.args.categorical not in ['onehot','numbers']:
				self.args.log.write(f"\nx  The categorical option used is not valid! Options: 'onehot', 'numbers'")
				curate_valid = False

			elif self.args.thres_x > 1 or self.args.thres_x < 0:
				self.args.log.write(f"\nx  The thres_x option should be between 0 and 1!")
				curate_valid = False

			elif self.args.thres_y > 1 or self.args.thres_y < 0:
				self.args.log.write(f"\nx  The thres_y option should be between 0 and 1!")
				curate_valid = False
		
		elif type_checks == 'csv_db':
			if self.args.y not in columns_csv:
				self.args.log.write(f"\nx  The thres_y option specified ({self.args.y}) is not a columnd in the csv selected ({self.args.csv_name})!")
				curate_valid = False

			for val in self.args.discard:
				if val not in columns_csv:
					self.args.log.write(f"\nx  Descriptor {val} specified in the discard option is not a columnd in the csv selected ({self.args.csv_name})!")
					curate_valid = False

		if not curate_valid:
			self.args.log.finalize()
			sys.exit()


	def categorical_transform(self,csv_df):
		# converts all columns with strings into categorical values (one hot encoding
		# by default, can be set to numerical 1,2,3... with categorical = True).
		# Troubleshooting! For one-hot encoding, don't use variable names that are
		# also column headers! i.e. DESCRIPTOR "C_atom" contain C2 as a value,
		# but C2 is already a header of a different column in the database. Same applies
		# for multiple columns containing the same variable names.

		self.args.log.write(f'\no  Analyzing categorical variables.')

		descriptors_to_drop, categorical_vars = [],[]
		for column in csv_df.columns:
			if column not in self.args.discard and column not in self.args.y:
				if(csv_df[column].dtype == 'object'):
					descriptors_to_drop.append(column)
					categorical_vars.append(column)
					if self.args.categorical == 'numbers':
						csv_df[column] = csv_df[column].astype('category')
						csv_df[column] = csv_df[column].cat.codes
					else:
						_ = csv_df[column].unique() # is this necessary?
						dummies = pd.get_dummies(csv_df[column])
						csv_df = csv_df.drop(column, axis=1)
						csv_df = pd.concat([csv_df, dummies], axis=1)

		if len(categorical_vars) == 0:
			self.args.log.write(f'\no  No categorical variables were found.')
		else:
			self.args.log.write(f'\no  A total of {len(categorical_vars)} categorical variables were converted using the {self.args.categorical} mode in the categorical option:')
			print_cat = '\n   '.join(var for var in categorical_vars)
			self.args.log.write(f'{print_cat}')

		return csv_df


	def correlation_filter(self, csv_df):
		"""
		Discards a) correlated variables and b) variables that do not correlate with the y values, based
		on R**2 values.
		"""

		self.args.log.write(f'\no  Correlation filter activated with these thresholds: thres_x = {self.args.thres_x}, thres_y = {self.args.thres_y}')
		self.args.log.write(f'\nExcluded descriptors:')

		descriptors_drop = []
		for i,column in enumerate(csv_df.columns):
			if column not in descriptors_drop and column != self.args.y:
				# finds the descriptors with low correlation to the response values
				_, _, r_value_y, _, _ = stats.linregress(csv_df[column],csv_df[self.args.y])
				rsquared_y = r_value_y**2
				if rsquared_y < self.args.thres_y:
					descriptors_drop.append(column)
					self.args.log.write(f'{column}: R**2 = {round(rsquared_y,2)} with the {self.args.y} values')
				# finds correlated descriptors
				if column != csv_df.columns[-1]:
					for j,column2 in enumerate(csv_df.columns):
						if j > i and column2 not in descriptors_drop and column2 != self.args.y:
							_, _, r_value_x, _, _ = stats.linregress(csv_df[column],csv_df[column2])
							rsquared_x = r_value_x**2
							if rsquared_x > self.args.thres_x:
								# discard the column with less correlation with the y values
								_, _, r_value_y2, _, _ = stats.linregress(csv_df[column2],csv_df[self.args.y])
								rsquared_y2 = r_value_y2**2
								if rsquared_y >= rsquared_y2:
									descriptors_drop.append(column2)
									self.args.log.write(column2,': R**2 = '+str(round(rsquared_x,2))+' with '+column)
								else:
									descriptors_drop.append(column)
									self.args.log.write(column,': R**2 = '+str(round(rsquared_x,2))+' with '+column2)
		
		if len(descriptors_drop) == 0:
			self.args.log.write(f'\no  No descriptors were removed')
	
		# drop descriptors that did not pass the filters
		csv_df_filtered = csv_df.drop(descriptors_drop, axis=1)

		self.args.log.write(f'\n\no  {csv_df_filtered.columns} descriptors remaining after applying correlation filters:')
		print_cat = '\n   '.join(var for var in csv_df_filtered.columns)
		self.args.log.write(f'{print_cat}')

		return csv_df_filtered
