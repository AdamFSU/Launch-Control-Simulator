#include "socketconnection.h"
#include <QDebug>
#include <QIODevice>
#include <QJsonDocument>
#include <QJsonObject>

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
    clientConnection = server->nextPendingConnection();
    connect(clientConnection, &QIODevice::readyRead, this, &SocketConnection::readData);
}

void SocketConnection::readData()
{
//    qDebug() << "There is data ready to be read";

    QByteArray byteArray;
    byteArray = clientConnection->readAll();
    // Converting QByteArray to QString
    QString dataAsString = QString::fromUtf8(byteArray);
    QJsonDocument doc = QJsonDocument::fromJson(byteArray);
    QJsonObject obj;
    QString process_name;
    double xValue = 0;
    double yValue = 0;
    if(doc.isObject())
    {
        obj = doc.object();
    }
    else
    {
        qDebug() << "Document is not a JSON Object";
    }
    if(obj.contains("name") && obj["name"].isString())
    {
        process_name = obj["name"].toString();
    }
    if(obj.contains("value1") && obj["value1"].isDouble())
    {
        xValue = obj["value1"].toDouble();
    }
    if(obj.contains("value2") && obj["value2"].isDouble())
    {
        yValue = obj["value2"].toDouble();
    }
//    float data = dataAsString.toFloat();
//    qDebug() << "conversion from qstring to float: " << data;
    emit new_data(process_name, xValue, yValue);
    qDebug().noquote() << "Qt data: " << dataAsString;
}

void SocketConnection::sendData(QString name)
{
    qDebug() << "Sending message to abort Launch!";
    QByteArray block;
    QDataStream out(&block, QIODevice::WriteOnly);
    QString jsonMessage;
    jsonMessage = "{\"name\": \"" + name + "\", \"status\": \"FAIL\"}";

    out << jsonMessage;

    clientConnection->write(block);
}
