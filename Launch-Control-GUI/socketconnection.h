#ifndef SOCKETCONNECTION_H
#define SOCKETCONNECTION_H

#include <QObject>
#include <QTcpServer>
#include <QHostAddress>
#include <QTcpSocket>
#include <QDataStream>

class SocketConnection : public QObject
{
    Q_OBJECT
public:
    explicit SocketConnection(QObject *parent = nullptr);

signals:
    void new_data(QString name, double xValue, double yValue);

public slots:
    void establishConnection();
    void disconnected();
    void connectionEstablished();
    void readData();
    void sendData(QString name);

private:
    QTcpServer *server;
    QTcpSocket *clientConnection;

};

#endif // SOCKETCONNECTION_H
