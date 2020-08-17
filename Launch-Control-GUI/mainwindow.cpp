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
    connect(conn, &SocketConnection::new_data, this, &MainWindow::display_new_data);
    thread->start();

    // create graph and assign data to it
    ui->customPlot->addGraph();
    // give the axes some labels
    ui->customPlot->xAxis->setLabel("x");
    ui->customPlot->yAxis->setLabel("y");
    // set axes ranges, so we see all data:
    ui->customPlot->xAxis->setRange(0, 50);
    ui->customPlot->yAxis->setRange(0, 5);
    ui->customPlot->replot();
}

void MainWindow::display_new_data(float data)
{
    qDebug() << "updating graph!" << data;
    ui->customPlot->graph(0)->addData(data, 2);
    ui->customPlot->replot();
}

MainWindow::~MainWindow()
{
    delete ui;
}

