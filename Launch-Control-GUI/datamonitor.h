#ifndef DATAMONITOR_H
#define DATAMONITOR_H
#include <QObject>


class DataMonitor : public QObject
{
    Q_OBJECT
public:
    explicit DataMonitor(QObject *parent = nullptr);

signals:
    void check_failed(QString name);

public slots:
    void monitorData(QString name, double xValue, double yValue);

private:

};

#endif // DATAMONITOR_H
