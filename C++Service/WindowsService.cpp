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
//	servicestatus.dwControlsAccepted = SERVICE_ACCEPT_SHUTDOWN | SERVICE_ACCEPT_STOP;//�ڱ�����ֻ����ϵͳ�ػ���ֹͣ�������ֿ�������
//	servicestatus.dwWin32ExitCode = 0;
//	servicestatus.dwServiceSpecificExitCode = 0;
//	servicestatus.dwCheckPoint = 0;
//	servicestatus.dwWaitHint = 0;
//
//	//ע�������ƴ���������������ָ��ControlHandlerfunction ��ָ�룩������״̬������ SCM ��������
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
//	//��SCM ��������״̬
//	SetServiceStatus(hstatus, &servicestatus);
//
//	//����Ϳ�ʼ����ѭ���ˣ������������Լ�ϣ���������Ĺ���
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
//	entrytable[0].lpServiceName = (LPWSTR)L"userAndGroup";//������
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
