#ifndef SOCKETCONNECTION_H
#define SOCKETCONNECTION_H

#include <QObject>
#include <QTcpServer>
#include <QHostAddress>

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

private:
    QTcpServer *server;

};

#endif // SOCKETCONNECTION_H
