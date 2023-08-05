import huble
from huble import Dataset
def run_experiment(experiment):
	model = huble.sklearn.svm_svc(parameters={'C': 1, 'kernel': 'rbf', 'probability': False, 'random_state': None, 'max_iter': -1, 'decision_function_shape': 'ovr', 'tol': 0})
	data = Dataset('https://ipfs.filebase.io/ipfs/QmRspeqXi9J2PVTmXYwMaBif9dYWVkNhM8EFomUAfajnT1').dataframe
	training_dataset, test_dataset, input_format = huble.sklearn.train_test_split(data=data,parameters={'test_size': 0.2}, target_column='Cabin')
	Model, filename = huble.sklearn.train_model(data=training_dataset, model=model, column='Survived', task_type='clustering')
	metrics = huble.sklearn.evaluate_model(model=Model, training_dataset=training_dataset, test_dataset=test_dataset, target_column= 'Cabin', task_type='clustering' )
	experiment.upload_metrics(metrics,input_format)
	print("Uploading model...")
	experiment.upload_model(filename)