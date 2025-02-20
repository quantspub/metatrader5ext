// main.cpp : Defines the entry point for the DLL application.
#pragma once
#include "pch.h"
#include "stdafx.h"
#include "microsvc_controller.hpp"

using namespace web;
using namespace cfx;
using namespace utility;

// #ifdef MT_EXPFUNC_EXPORTS
// #define MT_EXPFUNC __declspec(dllexport)
// #else
// #define MT_EXPFUNC __declspec(dllimport)
// #endif
#define MT_EXPFUNC extern "C" __declspec(dllexport)

#define dbg(msg) writeLog(L"D:\\rest.log", msg);

#define dbgs(msg)                                  \
	string cs(e.what());                           \
	wstring ws;                                    \
	copy(cs.begin(), cs.end(), back_inserter(ws)); \
	dbg(ws.c_str());

static MicroserviceController server;

int writeLog(const wchar_t *file, const wchar_t *content)
{
	if (file && content)
	{
		FILE *fd;
		errno_t err = _wfopen_s(&fd, file, L"a+b");
		if (err != 0)
			return 1;
		else
		{
			SYSTEMTIME st;
			GetLocalTime(&st);
			fwprintf(fd, L"%04d.%02d.%02d %02d:%02d:%02d.%03d::%s\r\n",
					 st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds, content);

			fclose(fd);
		}
	}
	return 0;
}

MT_EXPFUNC int __stdcall Init(const char *url, int port, int command_wait_timeout, const char *path, const char *url_swagger)
{

	try
	{
		// utility::string_t address = U("http://host_auto_ip4:");
		string t(url);
		utility::string_t address;
		copy(t.begin(), t.end(), back_inserter(address));
		address.append(L":");
		address.append(to_wstring(port));

		server.setEndpoint(address);
		dbg(server.endpoint().c_str());

		server.setCommandWaitTimeout(command_wait_timeout);
		server.setPath(path, url_swagger);

		// wait for server initialization...
		server.accept().wait();
		dbg(L"started");
	}
	catch (std::exception &e)
	{
		std::cerr << "something wrong happened! " << std::endl;
		std::cerr << e.what() << std::endl;
		server.pushCommand(L"failed", s2ws(e.what()));
		dbgs(e.what());
	}
	catch (...)
	{
	}

	return 1;
}

MT_EXPFUNC void __stdcall Deinit()
{
	try
	{
		server.shutdown().wait();
	}
	catch (std::exception &e)
	{
		std::cerr << e.what() << std::endl;
		dbgs(e.what());
	}
	catch (...)
	{
	}
}

MT_EXPFUNC int __stdcall GetCommand(char *data)
{

	if (!server.hasCommands())
		return 0;

	strcpy(data, server.getCommand());
	strcat(data, "\0");

	return 1;
}

MT_EXPFUNC int __stdcall SetCommandResponse(const char *command, const char *response)
{
	server.setCommandResponse(command, response);
	return 1;
}

MT_EXPFUNC int __stdcall SetCallback(const char *url, const char *format)
{
	server.setCallback(url, format);
	return 1;
}

MT_EXPFUNC int __stdcall RaiseEvent(const char *data)
{

	server.onEvent(data);

	return 1;
}

MT_EXPFUNC int __stdcall SetAuthToken(const char *token)
{

	server.setAuthToken(token);

	return 1;
}