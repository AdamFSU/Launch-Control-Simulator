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
    void new_data(float graph_data);

public slots:
    void establishConnection();
    void disconnected();
    void connectionEstablished();
    void readData();

private:
    QTcpServer *server;
    QTcpSocket *clientConnection;
    QDataStream in;

};

#endif // SOCKETCONNECTION_H
