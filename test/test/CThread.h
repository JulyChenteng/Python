#ifndef _CTHREAD_H_
#define _CTHREAD_H_

#include <signal.h>
#include <pthread.h>

#ifndef INVALID_THREAD
#define INVALID_THREAD ((pthread_t)(-1)
#endif

class CThread
{
  public:
    CThread(pthread_attr_t *attr = NULL);
    CThread(const pthread_t &th);
    CThread(const CThread &th);
    CThread &operator=(const CThread &th);
    virtual ~CThread();

  public:
    virtual int Start();
    virtual int Stop();
    int Terminate();
    int DetachSelf();
    bool IsRun();

  public:
    bool Attach(pthread_t pId);
    pthread_t Detach();
    bool IsValid() const {return INVALID_THREAD != m_pthread} pthread_t GetId() const { return m_pthread; }

  public:
    static void self(CThread &th) { th.Attach(pthread_self()); }

  protected:
    virtual void *Run() = 0;

  private:
    static void SigQuit(int signum);
    static void *Func(void *arg);

  private:
    pthread_t m_pthread;
    pthread_attr_t *m_pthAttr;
};

#endif