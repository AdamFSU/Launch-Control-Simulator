#ifndef SOCKETCONNECTION_H
#define SOCKETCONNECTION_H

#include <QObject>
#include <QTcpServer>
#include <QHostAddress>
#include <QTcpSocket>

class SocketConnection : public QObject
{
    Q_OBJECT
public:
    explicit SocketConnection(QObject *parent = nullptr);

signals:

public slots:
    void establishConnection();
    void disconnected();
    void connectionEstablished();
    void readData();

private:
    QTcpServer *server;
    QTcpSocket *clientConnection;

};

#endif // SOCKETCONNECTION_H
