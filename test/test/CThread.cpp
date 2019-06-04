#include "CThread.h"

CThread::CThread(pthread_attr_t* attr) : 
    m_pthread(INVALID_THREAD),
    m_pthAttr(NULL)
{
    if (NULL != attr)
    {
        m_pthAttr = new pthread_attr_t;
        *m_pthAttr = attr;
    }
}

CThread::CThread(const CThread& th)
{
    if (&th == this)
    {
        return;
    }

    Detach();

    m_pthread = th.m_pthread;
    m_pthAttr = th.m_pthAttr;
    *m_pthAttr = *th.m_pthAttr;
}

CThread::CThread(const pthread_t &th) : 
    m_pthread(th), 
    m_pthAttr(NULL)
{

}

CThread& CThread::operator=(const CThread& th)
{
    if (&th == this)
    {
        return *this;
    }

    Detach();

    m_pthread = th.m_pthread;
    m_pthAttr = th.m_pthAttr;
    *m_pthAttr = *th.m_pthAttr;

    return *this;
}

CThread::~CThread()
{
    m_pthread = INVALID_THREAD;
    delete m_pthAttr;
    m_pthAttr = NULL;
}

int CThread::Start()
{
    const int nRet = pthread_create(&m_pthread, m_pthAttr, Func, (void*)this);
    if (nRet)
    {
        return -1;
    }

    return nRet;
}

int CThread::DetachSelf() 
{
    assert(INVALID_THREAD != m_pthread);

    pthread_detach(m_pthread);
    return m_thread;
}

int CThread::Stop()
{
    assert(IsValid());
    if (IsRun())
    {
        pthread_kill(m_pthread, SIGQUIT);
    }

    return 0;
}

int CThread::Terminate()
{
    return -1;
}

bool CThread::IsRun()
{
    assert(INVALID_THREAD != m_pthread);

    if (ESRCH != pthread_kill(m_pthread, 0))
    {
        return true;
    }

    return false;
}

bool CThread::Attach(pthread_t pthId) 
{
    Detach();

    m_pthread = pthId;
    return true;
}

bool CThread::Detach()
{
    if (IsValid())
    {
        m_pthread = INVALID_THREAD;
        delete m_pthAttr;
        m_pthAttr = NULL;
    }
}

void CThread::SigQuit(int signum)
{
    pthread_exit(NULL);
}

void* CThread::Func(void* arg)
{
    CThread *th = (CThread *)arg;

    return th->Run();
}