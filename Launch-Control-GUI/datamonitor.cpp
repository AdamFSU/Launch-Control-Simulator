#include "datamonitor.h"
#include <QDebug>

DataMonitor::DataMonitor(QObject *parent) : QObject(parent)
{

}

void DataMonitor::monitorData(QString name, double xValue, double yValue)
{
    qDebug() << "Monitoring data!!!....";
    if(xValue > 24 && yValue > 49)
    {
        emit check_failed(name);
    }
}
