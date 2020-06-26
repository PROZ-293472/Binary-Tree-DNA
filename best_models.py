import pickle

best_a_model = pickle.load(open("models//acceptor//r=400_k=2_o=0.001.p", "rb"))
best_d_model = pickle.load(open("models//donor//r=400_k=2_o=0.1.p", "rb"))
best_a_model.show_test_accuracies()
best_d_model.show_test_accuracies()
best_a_model.show_train_accuracies()
best_d_model.show_train_accuracies()
