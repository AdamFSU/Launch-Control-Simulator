#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <QThread>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QThread * thread = new QThread;
    SocketConnection * conn = new SocketConnection;
    conn->moveToThread(thread);
    connect(thread, SIGNAL(started()), conn, SLOT(establishConnection()));
    thread->start();

    QVector<double> x(101), y(101);
    for (int i=0; i<101; ++i)
    {
        x[i] = i/50.0 - 1;
        y[i] = x[i]*x[i];
    }
    // create graph and assign data to it
    ui->customPlot->addGraph();
    ui->customPlot->graph(0)->setData(x, y);
    // give the axes some labels
    ui->customPlot->xAxis->setLabel("x");
    ui->customPlot->yAxis->setLabel("y");
    // set axes ranges, so we see all data:
    ui->customPlot->xAxis->setRange(-1, 1);
    ui->customPlot->yAxis->setRange(0, 1);
    ui->customPlot->replot();
}

MainWindow::~MainWindow()
{
    delete ui;
}

