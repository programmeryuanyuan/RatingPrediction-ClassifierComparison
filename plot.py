
import itertools
import re
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np


def plot_confusion_matrix(y_original, y_predicted, classes,
                          ml_name, title='Confusion matrix',
                          cmap=plt.cm.Blues):

    cm = confusion_matrix(y_original, y_predicted)

    plt.figure()

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'g'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig(ml_name + '_CM.png', bbox_inches='tight')
    plt.show()
    plt.close()


def plot_classification_report(y_original, y_predicted, classes,
                               ml_name, title='Classification report',
                               cmap='RdBu'):

    classificationReport = classification_report(
        y_original, y_predicted, target_names=classes, digits=4,zero_division=0)#,zero_division=0

    lines = classificationReport.replace('\n\n', '\n').split('\n')
    lines = [s for s in lines if not any(s in e for e in ['micro avg', 'macro avg'])]
    class_names, plotMat, support = [], [], []
    for line in lines[1:-3] + [lines[-1]]:
        t = re.split(r'\s{2,}', line.strip())
        if len(t) < 2:
            continue
        class_names.append(t[0])
        v = [float(x) for x in t[1:-1]]
        support.append(int(t[-1]))
        plotMat.append(v)

    plotMat = np.array(plotMat)
    xticklabels = ['Precision', 'Recall', 'F1-score']
    yticklabels = ['{0} ({1})'.format(class_names[idx], sup)
                   for idx, sup in enumerate(support)]

    plt.imshow(plotMat, interpolation='nearest', cmap=cmap, aspect='auto')
    plt.title(title)
    plt.colorbar()
    plt.xticks(np.arange(3), xticklabels, rotation=45)
    plt.yticks(np.arange(len(class_names)), yticklabels)

    upper_thresh = plotMat.min() + (plotMat.max() - plotMat.min()) / 10 * 8
    lower_thresh = plotMat.min() + (plotMat.max() - plotMat.min()) / 10 * 2
    for i, j in itertools.product(range(plotMat.shape[0]), range(plotMat.shape[1])):
        plt.text(j, i, format(plotMat[i, j], '.3f'),
                 horizontalalignment="center",
                 color="black" if upper_thresh > plotMat[i, j] > lower_thresh else "white")

    plt.ylabel('Metrics')
    plt.xlabel('Classes')

    plt.tight_layout()
    plt.savefig(ml_name + '_CR.png', bbox_inches='tight')
    plt.show()
    plt.close()