
#ifndef _KP_H_
#define _KP_H_

#include "ontology.h"
#include <stdlib.h>
#include <errno.h>
#include <jni.h>
#include <string.h>

#define MAX_CLASS_NAME_LENGTH 20
#define ERROR_MSG_LENGTH 40
#define MAX_PROPERTIES 10

JavaVM* JVM;

individual_t *personProfile;
individual_t *currentSection;
individual_t *temp_ind;
individual_t *head;    //queue
prop_val_t *head_username;

list_t *hasVideoPropList;
list_t *hasHeadPropList;     //queue
list_t* getHeadList();  //queue
list_t* getRequestList();   //queue

jclass *classAgenda;
jclass *classProjector;
jclass *classKP;
jclass *classQueueService;  //queue
jclass *classQueueHead;  //queue
jclass *classMicService;

jobject *agendaClassObject;
jobject *presentationClassObject;
jobject *queueClassObject;


subscription_t *conferenceSubscriptionContainer;
subscription_t *presentationSubscriptionContainer;
subscription_t *conferenceClassSubscriptionContainer;
subscription_t *presentationClassSubscriptionContainer;
subscription_t *headsub;    //queue

char *startedVideoUuid;
const char *message1;
const char *message2;
const char *message3;
const char *message4;
const char *message5;
const char *headUsername = "user";
const char *GlobalUsername;

int currentTimeslotIndex;
int hasVideoPropListLen;
int hasHeadPropListLen;     //queue

void addTimeslotToJavaList(JNIEnv *, individual_t *, jobject);
void subscriptionHandler(subscription_t *);
void projectorNotificationHandler(subscription_t *);
void agendaNotificationHandler(subscription_t *);
void conferenceNotificationHandler(subscription_t *);
void headHandler(subscription_t *);     //queue
void logout();
int getListSize(list_t*);
int subscribeConferenceService();
int subscribePresentationService();
int subscribeQueueService();    //queue
int subscribeQueueHead();    //queue
int calculateTimeslotIndex(prop_val_t *);
int searchPerson(individual_t *, const char *, const char *);
int activatePerson(individual_t *);
char* generateUuid(char*);
bool personExists(const char *);
bool placeExists(const char *);
bool requestExists(const char *);   //queu

jclass getJClassObject(JNIEnv *, char *);
jfieldID getFieldID(JNIEnv *, jclass, char *, char *);
prop_val_t* initNullProperty();
prop_val_t* getPresentationTitleProp(individual_t*);
individual_t* createProfile(individual_t *);
individual_t* createPerson(const char *, const char *, const char*);
individual_t* getTimeslot(int);
individual_t* getCurrentSection();
individual_t* getFirstTimeslot();
individual_t* getContentService();
individual_t* getExistingSection();
individual_t* createPlace(const char *);
list_t* getVideoList();


individual_t* createRequest(const char *, const char *);    //queue
individual_t* createHead(const char *);     //queue

#endif
