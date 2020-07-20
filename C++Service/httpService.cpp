// httpService.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include "HttpService.h"
#include <iostream>
#include <cstring>
#include <atlstr.h>
using namespace std;

struct mg_serve_http_opts HttpService::s_http_server_opts;

string StringToUtf(string strValue)
{

    int nwLen = MultiByteToWideChar(CP_UTF8, 0, strValue.c_str(), -1, NULL, 0);
    wchar_t* pwBuf = new wchar_t[nwLen + 1];//加上末尾'\0'
    memset(pwBuf, 0, nwLen * 2 + 2);
    MultiByteToWideChar(CP_UTF8, 0, strValue.c_str(), strValue.length(), pwBuf, nwLen);
    int nLen = WideCharToMultiByte(CP_ACP, 0, pwBuf, -1, NULL, NULL, NULL, NULL);
    char* pBuf = new char[nLen + 1];
    memset(pBuf, 0, nLen + 1);
    WideCharToMultiByte(CP_ACP, 0, pwBuf, nwLen, pBuf, nLen, NULL, NULL);
    std::string retStr = pBuf;
    delete[]pBuf;
    delete[]pwBuf;
    return retStr;

}

string UtfToString(string strValue)

{

    int nwLen = ::MultiByteToWideChar(CP_ACP, 0, strValue.c_str(), -1, NULL, 0);
    wchar_t* pwBuf = new wchar_t[nwLen + 1];//加上末尾'\0'
    ZeroMemory(pwBuf, nwLen * 2 + 2);
    ::MultiByteToWideChar(CP_ACP, 0, strValue.c_str(), strValue.length(), pwBuf, nwLen);
    int nLen = ::WideCharToMultiByte(CP_UTF8, 0, pwBuf, -1, NULL, NULL, NULL, NULL);
    char* pBuf = new char[nLen + 1];
    ZeroMemory(pBuf, nLen + 1);
    ::WideCharToMultiByte(CP_UTF8, 0, pwBuf, nwLen, pBuf, nLen, NULL, NULL);
    std::string retStr(pBuf);
    delete[]pwBuf;
    delete[]pBuf;
    pwBuf = NULL;
    pBuf = NULL;
    return retStr;
}

std::wstring UTF8ToWString(const char* lpcszString)
{
    int len = strlen(lpcszString);
    int unicodeLen = ::MultiByteToWideChar(CP_UTF8, 0, lpcszString, -1, NULL, 0);
    wchar_t* pUnicode;
    pUnicode = new wchar_t[unicodeLen + 1];
    memset((void*)pUnicode, 0, (unicodeLen + 1) * sizeof(wchar_t));
    ::MultiByteToWideChar(CP_UTF8, 0, lpcszString, -1, (LPWSTR)pUnicode, unicodeLen);
    std::wstring wstrReturn(pUnicode);
    delete[] pUnicode;
    return wstrReturn;
}

static std::string UTF8ToGBK(const char* strUTF8)
{
    int len = MultiByteToWideChar(CP_UTF8, 0, strUTF8, -1, NULL, 0);
    wchar_t* wszGBK = new wchar_t[len + 1];
    memset(wszGBK, 0, len * 2 + 2);
    MultiByteToWideChar(CP_UTF8, 0, strUTF8, -1, wszGBK, len);
    len = WideCharToMultiByte(CP_ACP, 0, wszGBK, -1, NULL, 0, NULL, NULL);
    char* szGBK = new char[len + 1];
    memset(szGBK, 0, len + 1);
    WideCharToMultiByte(CP_ACP, 0, wszGBK, -1, szGBK, len, NULL, NULL);
    std::string strTemp(szGBK);

    if (wszGBK) delete[] wszGBK;
    if (szGBK) delete[] szGBK;

    return strTemp;
}


//请求事件处理
void HttpService::mgEvHandler(struct mg_connection* nc, int ev, void* p) {
    //处理request
    if (ev == MG_EV_HTTP_REQUEST) {
        struct http_message* msg = (struct http_message*)p;
        //request方法
        char* method = new char[msg->method.len + 1];
        memset(method, 0, msg->method.len + 1);
        memcpy(method, msg->method.p, msg->method.len);
        std::cout << "打印method " << method << std::endl;

        //query内容
        char* query = new char[msg->query_string.len + 1];
        memset(query, 0, msg->query_string.len + 1);
        memcpy(query, msg->query_string.p, msg->query_string.len);
        std::cout << "打印query " << query << std::endl;
        char n2[250];
        mg_get_http_var(&msg->query_string, "name", &n2[0], sizeof(n2));
        wstring ws = UTF8ToWString(n2);
        wcout.imbue(locale("chs"));
        std::wcout << L"打印id " << ws << std::endl;
        //body内容
        char* body = new char[msg->body.len + 1];
        memset(body, 0, msg->body.len + 1);
        memcpy(body, msg->body.p, msg->body.len);
        printf("打印body %s \n", body);

        //uri内容
        char* uri = new char[msg->uri.len + 1];
        memset(uri, 0, msg->uri.len + 1);
        memcpy(uri, msg->uri.p, msg->uri.len);
        printf("打印uri %s \n", uri);

        //返回body信息
        mgSendBody(nc, "body content");
        //返回下载文件
        //mgSendFile("相对于s_http_server_opts.document_root的文件路径");

        delete uri;
        delete body;
        delete method;
        delete query;
    }
}

//发送body信息
void HttpService::mgSendBody(struct mg_connection* nc, const char* content) {
    mg_send_head(nc, 200, strlen(content), "Content-Type: text/plain\r\nConnection: close");
    mg_send(nc, content, strlen(content));
    nc->flags |= MG_F_SEND_AND_CLOSE;
}

//发送文件，文件的位置是相对于s_http_server_opts.document_root的路径
void HttpService::mgSendFile(struct mg_connection* nc, struct http_message* hm, const char* filePath) {
    mg_http_serve_file(nc, hm, filePath, mg_mk_str("text/plain"), mg_mk_str(""));
}

//初始化并启动
bool HttpService::start(const char* port) {
    struct mg_mgr mgr;
    struct mg_connection* nc;

    mg_mgr_init(&mgr, NULL);
    printf("Starting web server on port %s\n", port);
    nc = mg_bind(&mgr, port, mgEvHandler);
    if (nc == NULL) {
        printf("Failed to create listener\n");
        return false;
    }

    // Set up HTTP server parameters
    mg_set_protocol_http_websocket(nc);
    s_http_server_opts.document_root = ".";  //文件相对路径 Serve current directory
    s_http_server_opts.enable_directory_listing = "yes";

    for (;;) {
        mg_mgr_poll(&mgr, 1000); //1s轮训一次
    }
    mg_mgr_free(&mgr);

    return true;
}


int main(int argc, char* argv[])
{
    HttpService* httpService = new HttpService();
    httpService->start("8000");
    std::cout << "Hello World!\n";
}