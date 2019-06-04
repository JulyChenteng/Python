#ifndef _CTHREAD_LOCK_H_
#define _CTHREAD_LOCK_H_

#include <pthread.h>

class CThreadLock
{
public:
    CThreadLock() { pthread_mutex_init(&m_lock, NULL); }
    ~CThreadLock() { pthread_mutex_destroy(&m_lock); }

    int32 lock() { return pthread_mutex_lock(&m_lock); }
    int32 unlock() { return pthread_mutex_unlock(&m_lock); }
    int32 trylock() { return pthread_mutex_trylock(&m_lock); }

private:
    pthread_mutex_t m_lock;
};

#endif
