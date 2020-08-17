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
    ui->customPlot->yAxis->setRange(0, 100);
    ui->customPlot->replot();

    ui->customPlot2->addGraph();
    ui->customPlot2->xAxis->setLabel("x");
    ui->customPlot2->yAxis->setLabel("y");
    ui->customPlot2->xAxis->setRange(0, 50);
    ui->customPlot2->yAxis->setRange(0, 100);
    ui->customPlot2->replot();
}

void MainWindow::display_new_data(QString name, double xValue, double yValue)
{
//    qDebug() << "updating graph!" << name << "xValue: " << xValue << "yValue: " << yValue;
    if(name == "M1D Hydraulic Pressurization")
    {
        ui->customPlot->graph(0)->addData(xValue, yValue);
        ui->customPlot->replot();
    }
    if(name == "LOX Fueling")
    {
        ui->customPlot2->graph(0)->addData(xValue, yValue);
        ui->customPlot2->replot();
    }

}

MainWindow::~MainWindow()
{
    delete ui;
}

