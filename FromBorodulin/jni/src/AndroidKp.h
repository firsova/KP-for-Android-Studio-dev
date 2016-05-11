/* DO NOT EDIT THIS FILE - it is machine generated */
#include <jni.h>
/* Header for class petrsu_smartroom_android_srcli_KP */

#ifndef _Included_petrsu_smartroom_android_srcli_KP
#define _Included_petrsu_smartroom_android_srcli_KP
#ifdef __cplusplus
extern "C" {
#endif
#undef petrsu_smartroom_android_srcli_KP_MODE_PRIVATE
#define petrsu_smartroom_android_srcli_KP_MODE_PRIVATE 0L
#undef petrsu_smartroom_android_srcli_KP_MODE_WORLD_READABLE
#define petrsu_smartroom_android_srcli_KP_MODE_WORLD_READABLE 1L
#undef petrsu_smartroom_android_srcli_KP_MODE_WORLD_WRITEABLE
#define petrsu_smartroom_android_srcli_KP_MODE_WORLD_WRITEABLE 2L
#undef petrsu_smartroom_android_srcli_KP_MODE_APPEND
#define petrsu_smartroom_android_srcli_KP_MODE_APPEND 32768L
#undef petrsu_smartroom_android_srcli_KP_MODE_MULTI_PROCESS
#define petrsu_smartroom_android_srcli_KP_MODE_MULTI_PROCESS 4L
#undef petrsu_smartroom_android_srcli_KP_MODE_ENABLE_WRITE_AHEAD_LOGGING
#define petrsu_smartroom_android_srcli_KP_MODE_ENABLE_WRITE_AHEAD_LOGGING 8L
#undef petrsu_smartroom_android_srcli_KP_BIND_AUTO_CREATE
#define petrsu_smartroom_android_srcli_KP_BIND_AUTO_CREATE 1L
#undef petrsu_smartroom_android_srcli_KP_BIND_DEBUG_UNBIND
#define petrsu_smartroom_android_srcli_KP_BIND_DEBUG_UNBIND 2L
#undef petrsu_smartroom_android_srcli_KP_BIND_NOT_FOREGROUND
#define petrsu_smartroom_android_srcli_KP_BIND_NOT_FOREGROUND 4L
#undef petrsu_smartroom_android_srcli_KP_BIND_ABOVE_CLIENT
#define petrsu_smartroom_android_srcli_KP_BIND_ABOVE_CLIENT 8L
#undef petrsu_smartroom_android_srcli_KP_BIND_ALLOW_OOM_MANAGEMENT
#define petrsu_smartroom_android_srcli_KP_BIND_ALLOW_OOM_MANAGEMENT 16L
#undef petrsu_smartroom_android_srcli_KP_BIND_WAIVE_PRIORITY
#define petrsu_smartroom_android_srcli_KP_BIND_WAIVE_PRIORITY 32L
#undef petrsu_smartroom_android_srcli_KP_BIND_IMPORTANT
#define petrsu_smartroom_android_srcli_KP_BIND_IMPORTANT 64L
#undef petrsu_smartroom_android_srcli_KP_BIND_ADJUST_WITH_ACTIVITY
#define petrsu_smartroom_android_srcli_KP_BIND_ADJUST_WITH_ACTIVITY 128L
#undef petrsu_smartroom_android_srcli_KP_CONTEXT_INCLUDE_CODE
#define petrsu_smartroom_android_srcli_KP_CONTEXT_INCLUDE_CODE 1L
#undef petrsu_smartroom_android_srcli_KP_CONTEXT_IGNORE_SECURITY
#define petrsu_smartroom_android_srcli_KP_CONTEXT_IGNORE_SECURITY 2L
#undef petrsu_smartroom_android_srcli_KP_CONTEXT_RESTRICTED
#define petrsu_smartroom_android_srcli_KP_CONTEXT_RESTRICTED 4L
#undef petrsu_smartroom_android_srcli_KP_RESULT_CANCELED
#define petrsu_smartroom_android_srcli_KP_RESULT_CANCELED 0L
#undef petrsu_smartroom_android_srcli_KP_RESULT_OK
#define petrsu_smartroom_android_srcli_KP_RESULT_OK -1L
#undef petrsu_smartroom_android_srcli_KP_RESULT_FIRST_USER
#define petrsu_smartroom_android_srcli_KP_RESULT_FIRST_USER 1L
#undef petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_DISABLE
#define petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_DISABLE 0L
#undef petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_DIALER
#define petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_DIALER 1L
#undef petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_SHORTCUT
#define petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_SHORTCUT 2L
#undef petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_SEARCH_LOCAL
#define petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_SEARCH_LOCAL 3L
#undef petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_SEARCH_GLOBAL
#define petrsu_smartroom_android_srcli_KP_DEFAULT_KEYS_SEARCH_GLOBAL 4L
/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    connectSmartSpace
 * Signature: (Ljava/lang/String;Ljava/lang/String;I)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_connectSmartSpace
  (JNIEnv *, jclass, jstring, jstring, jint);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    loadTimeslotList
 * Signature: (Lpetrsu/smartroom/android/srcli/Agenda;)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_loadTimeslotList
  (JNIEnv *, jclass, jobject);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    disconnectSmartSpace
 * Signature: ()V
 */
JNIEXPORT void JNICALL Java_petrsu_smartroom_android_srcli_KP_disconnectSmartSpace
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getServicesInfo
 * Signature: (Lpetrsu/smartroom/android/srcli/ServicesMenu;)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_getServicesInfo
  (JNIEnv *, jclass, jobject);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    userRegistration
 * Signature: (Ljava/lang/String;Ljava/lang/String;)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_userRegistration
  (JNIEnv *, jclass, jstring, jstring);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    loadPresentation
 * Signature: (Lpetrsu/smartroom/android/srcli/Projector;)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_loadPresentation
  (JNIEnv *, jclass, jobject);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    initSubscription
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_initSubscription
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    startConference
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_startConference
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    endConference
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_endConference
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getProjectorClassObject
 * Signature: ()V
 */
JNIEXPORT void JNICALL Java_petrsu_smartroom_android_srcli_KP_getProjectorClassObject
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    showSlide
 * Signature: (I)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_showSlide
  (JNIEnv *, jclass, jint);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    endPresentation
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_endPresentation
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getCurrentTimeslotIndex
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_getCurrentTimeslotIndex
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    checkSpeakerState
 * Signature: ()Z
 */
JNIEXPORT jboolean JNICALL Java_petrsu_smartroom_android_srcli_KP_checkSpeakerState
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getMicServiceIP
 * Signature: ()Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getMicServiceIP
  (JNIEnv *, jclass);

/*
 * Class:	petrsu_smartroom_android_srcli_KP
 * Method:	getDiscussionServiceIP
 * Signature: ()Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getDiscussionServiceIP
	(JNIEnv *, jclass);

/*
 * Class:	petrsu_smartroom_android_srcli_KP
 * Method:	getSocialProgramServiceIP
 * Signature: ()Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getSocialProgramServiceIP
	(JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getMicServicePort
 * Signature: ()Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getMicServicePort
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getSpeakerName
 * Signature: ()Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getSpeakerName
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    personTimeslotIndex
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_personTimeslotIndex
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    checkConnection
 * Signature: ()Z
 */
JNIEXPORT jboolean JNICALL Java_petrsu_smartroom_android_srcli_KP_checkConnection
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getPresentationLink
 * Signature: (I)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getPresentationLink
  (JNIEnv *, jclass, jint);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    registerGuest
 * Signature: (Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_registerGuest
  (JNIEnv *, jclass, jstring, jstring, jstring);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    startConferenceFrom
 * Signature: (I)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_startConferenceFrom
  (JNIEnv *, jclass, jint);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    loadProfile
 * Signature: (Lpetrsu/smartroom/android/srcli/Profile;I)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_loadProfile
  (JNIEnv *, jclass, jobject, jint);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    saveProfileChanges
 * Signature: (Ljava/lang/String;Ljava/lang/String;)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_saveProfileChanges
  (JNIEnv *, jclass, jstring, jstring);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getPersonUuid
 * Signature: ()Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getPersonUuid
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    showVideo
 * Signature: (Ljava/lang/String;)I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_startVideo
  (JNIEnv *, jclass, jstring);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getVideoTitleList
 * Signature: ()[Ljava/lang/CharSequence;
 */
JNIEXPORT jobjectArray JNICALL Java_petrsu_smartroom_android_srcli_KP_getVideoTitleList
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getVideoUrlList
 * Signature: ()[Ljava/lang/CharSequence;
 */
JNIEXPORT jobjectArray JNICALL Java_petrsu_smartroom_android_srcli_KP_getVideoUuidList
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getContentUrl
 * Signature: ()Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getContentUrl
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    isActiveSubscriptions
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_isActiveSubscriptions
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    refreshConferenceSbcr
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_refreshConferenceSbcr
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    refreshPresentationSbcr
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_petrsu_smartroom_android_srcli_KP_refreshPresentationSbcr
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    getCurrentSectionList
 * Signature: ()[Ljava/lang/String;
 */
JNIEXPORT jobjectArray JNICALL Java_petrsu_smartroom_android_srcli_KP_getCurrentSectionList
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    sectionChanged
 * Signature: ()Z
 */
JNIEXPORT jboolean JNICALL Java_petrsu_smartroom_android_srcli_KP_sectionChanged
  (JNIEnv *, jclass);

/*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    closeVideo
 * Signature: ()V
 */
JNIEXPORT void JNICALL Java_petrsu_smartroom_android_srcli_KP_stopVideo
  (JNIEnv *, jclass);

 /*
 * Class:     petrsu_smartroom_android_srcli_KP
 * Method:    setPlaceInfo
 * Signature: ()[Ljava/lang/String;
 */
 JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_setPlaceInfo
  (JNIEnv *, jclass, jstring, jstring);

#ifdef __cplusplus
}
#endif
#endif
