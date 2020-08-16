#include "socketconnection.h"
#include <QDebug>

SocketConnection::SocketConnection(QObject *parent) : QObject(parent)
{

}

void SocketConnection::establishConnection()
{
    server = new QTcpServer(this);
    connect(server, SIGNAL(newConnection()), this, SLOT(connectionEstablished()));

    qDebug() << "connecting...";

    QHostAddress address("127.0.0.1");
    server->listen(address, 1234);
}

void SocketConnection::disconnected()
{
    qDebug() << "disconnected...";
}

void SocketConnection::connectionEstablished()
{
    qDebug() << "connection established!";
}
