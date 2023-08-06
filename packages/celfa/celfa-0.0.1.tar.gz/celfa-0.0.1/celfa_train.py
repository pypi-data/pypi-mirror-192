import celfa_data

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.callbacks import ModelCheckpoint


def train_model_no_mrd(charge_index, data_cont, model, name, path, datacontpath, bs, ep, save_only_test=True, chargeabs=False):
    train, val, test = celfa_data.load_and_create_train_val_test_sets(data_cont.data, data_cont.category_values)

    train_data, train_catvals = celfa_data.split_data_cat(train)
    train_data_cont = celfa_data.SimulationData(data=train_data,
                                                net_data_indices=data_cont.net_data_indices,
                                                stats_data_indices=data_cont.stats_data_indices,
                                                data_dict=data_cont.data_dict,
                                                input_layers=data_cont.input_layers,
                                                category_values=train_catvals,
                                                cat_values_dict=data_cont.cat_values_dict)
    if not save_only_test:
        celfa_data.save_data(f"{datacontpath}", f"{name}_train",
                             data=train_data_cont,
                             ending="pickle")
    train_data_charge = celfa_data.select_data(train_data, [charge_index])
    train_data_charge = np.array(train_data_charge)
    train_data_charge = train_data_charge.reshape((-1, 10, 16, 1))

    val_data, val_catvals = celfa_data.split_data_cat(val)
    valcont = celfa_data.SimulationData(data=val_data,
                                        net_data_indices=data_cont.net_data_indices,
                                        stats_data_indices=data_cont.stats_data_indices,
                                        data_dict=data_cont.data_dict,
                                        input_layers=data_cont.input_layers,
                                        category_values=val_catvals,
                                        cat_values_dict=data_cont.cat_values_dict)
    if not save_only_test:
        celfa_data.save_data(f"{datacontpath}", f"{name}_validation", data=valcont,
                             ending="pickle")

    val_data_charge = celfa_data.select_data(val_data, [charge_index])
    val_data_charge = np.array(val_data_charge)
    val_data_charge = val_data_charge.reshape((-1, 10, 16, 1))

    test_data, test_catval = celfa_data.split_data_cat(test)
    test_cont = celfa_data.SimulationData(data=test_data,
                                          net_data_indices=data_cont.net_data_indices,
                                          stats_data_indices=data_cont.stats_data_indices,
                                          data_dict=data_cont.data_dict,
                                          input_layers=data_cont.input_layers,
                                          category_values=test_catval,
                                          cat_values_dict=data_cont.cat_values_dict)
    celfa_data.save_data(f"{datacontpath}", f"{name}_test", data=test_cont,
                         ending="pickle")

    test_data_charge = celfa_data.select_data(test_data, [charge_index])
    test_data_charge = np.array(test_data_charge)
    test_data_charge = test_data_charge.reshape((-1, 10, 16, 1))

    train_catvals = np.array(train_catvals)
    val_catvals = np.array(val_catvals)
    test_catval = np.array(test_catval)

    # class_weight={0: 1., 1:2.}
    checkpoint = ModelCheckpoint(
        f"{path}{name}.model",
        monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')

    charge_map_layer_name = "charge_abs" if chargeabs else "charge"
    history = model.fit(
        {charge_map_layer_name: train_data_charge}, {"pred": train_catvals},
        validation_data=({charge_map_layer_name: val_data_charge}, {"pred": val_catvals}),
        batch_size=bs,
        shuffle=True,
        callbacks=[
            checkpoint
        ],
        epochs=ep)
    print(history.history.keys())

    plt_acchist(history)
    plt_loss(history)

    print("################################### \n \n Finished epochs \n \n ###################################")
    print("Testing...")
    fun_fin = tf.keras.models.load_model(f"{path}{name}.model")
    score = fun_fin.evaluate({charge_map_layer_name: test_data_charge}, {"pred": test_catval}, verbose=False)

    print('Test score (loss): ', score[0])  # Loss on test
    print('Test accuracy: ', score[1])
    return fun_fin


def plt_acchist(history, return_fa=False):
    fig, ax = plt.subplots(1, 1)
    ax.plot(history.history['accuracy'], label="Train")
    ax.plot(history.history['val_accuracy'], label="Validation")
    ax.set_title('Model accuracy')
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Epoch')
    ax.legend(loc='upper left')
    ax.grid()
    plt.show()
    if return_fa:
        return fig, ax


def plt_acchist_av(history, return_fa=False):
    fig, ax = plt.subplots(1, 1)
    acc = history.history['accuracy'][:]
    vacc = history.history['val_accuracy']

    acc = [*[np.average(acc[i*3:(i+1)*3]) for i in range(len(acc) - 3 + 1)], acc[-2], acc[-1]]
    vacc = [*[np.average(vacc[i*3:(i+1)*3]) for i in range(len(vacc) - 3 + 1)], vacc[-2], vacc[-1]]

    ax.plot(acc, label="Train")
    ax.plot(vacc, label="Validation")

    ax.set_title('Model accuracy')
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Epoch')
    ax.legend(loc='upper left')
    ax.grid()
    plt.show()
    if return_fa:
        return fig, ax


def plt_loss(history, return_fa=False):
    fig, ax = plt.subplots(1, 1)
    ax.plot(history.history['loss'], label="Train")
    ax.plot(history.history['val_loss'], label="Validation")
    ax.set_title('Model loss')
    ax.set_ylabel('Loss')
    ax.set_xlabel('Epoch')
    ax.legend(loc='upper left')
    ax.grid()
    plt.show()
    if return_fa:
        return fig, ax


def plt_loss_av(history, return_fa=False):
    fig, ax = plt.subplots(1, 1)
    loss = history.history['loss'][:]
    vloss = history.history['val_accuracy']

    loss = [*[np.average(loss[i * 3:(i + 1) * 3]) for i in range(len(loss) - 3 + 1)], loss[-2], loss[-1]]
    vloss = [*[np.average(vloss[i * 3:(i + 1) * 3]) for i in range(len(vloss) - 3 + 1)], vloss[-2], vloss[-1]]

    ax.plot(loss, label="Train")
    ax.plot(vloss, label="Validation")

    ax.set_title('Model loss')
    ax.set_ylabel('Loss')
    ax.set_xlabel('Epoch')
    ax.legend(loc='upper left')
    ax.grid()
    plt.show()
    if return_fa:
        return fig, ax
