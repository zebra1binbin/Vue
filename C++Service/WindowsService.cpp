//#include <iostream>
//#include <windows.h>
//
//bool brun = false;
//SERVICE_STATUS servicestatus;
//
//SERVICE_STATUS_HANDLE hstatus;
//
//
//void WINAPI ServiceMain(int argc, char** argv);
//
//void WINAPI CtrlHandler(DWORD request);
//
//
//void WINAPI ServiceMain(int argc, char** argv)
//{
//	servicestatus.dwServiceType = SERVICE_WIN32;
//	servicestatus.dwCurrentState = SERVICE_START_PENDING;
//	servicestatus.dwControlsAccepted = SERVICE_ACCEPT_SHUTDOWN | SERVICE_ACCEPT_STOP;//在本例中只接受系统关机和停止服务两种控制命令
//	servicestatus.dwWin32ExitCode = 0;
//	servicestatus.dwServiceSpecificExitCode = 0;
//	servicestatus.dwCheckPoint = 0;
//	servicestatus.dwWaitHint = 0;
//
//	//注册服务控制处理器（服务名和指向ControlHandlerfunction 的指针），控制状态器处理 SCM 控制请求
//	hstatus = ::RegisterServiceCtrlHandler(L"lsload", CtrlHandler);
//
//
//	if (hstatus == 0)
//	{
//		return;
//	}
//
//
//	servicestatus.dwCurrentState = SERVICE_RUNNING;
//	//向SCM 报告运行状态
//	SetServiceStatus(hstatus, &servicestatus);
//
//	//下面就开始任务循环了，你可以添加你自己希望服务做的工作
//
//	brun = true;
//
//	while (brun)
//	{
//
//	}
//
//}
//
//void WINAPI CtrlHandler(DWORD request)
//{
//	switch (request)
//	{
//	case SERVICE_CONTROL_STOP:
//		brun = false;
//		servicestatus.dwCurrentState = SERVICE_STOPPED;
//		break;
//
//	case SERVICE_CONTROL_SHUTDOWN:
//		brun = false;
//		servicestatus.dwCurrentState = SERVICE_STOPPED;
//		break;
//
//	default:
//		break;
//	}
//
//	SetServiceStatus(hstatus, &servicestatus);
//}
//
//
//int __cdecl wmain(int argc, char* argv[])
//{
//	SERVICE_TABLE_ENTRY entrytable[2];
//
//	entrytable[0].lpServiceName = (LPWSTR)L"userAndGroup";//服务名
//
//	entrytable[0].lpServiceProc = (LPSERVICE_MAIN_FUNCTION)ServiceMain;
//
//	entrytable[1].lpServiceName = NULL;
//
//	entrytable[1].lpServiceProc = NULL;
//
//	StartServiceCtrlDispatcher(entrytable);
//
//	return 0;
//}
//
