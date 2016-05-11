#include "AndroidKp.h"
#include "kp.h"
#include <android/log.h>



/**
 * @brief Extracts microphone service IP address
 *
 * @return IP address in success and NULL otherwise
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getMicServiceIP(
                                                                                 JNIEnv *env, jclass clazz) {
    
    list_t *list = sslog_ss_get_individual_by_class_all(CLASS_MICROPHONESERVICE);
    individual_t *individual;
    
    if(list != NULL) {
        list_head_t* pos = NULL;
        list_for_each(pos, &list->links) {
            list_t* node = list_entry(pos, list_t, links);
            individual = (individual_t*)(node->data);
            sslog_ss_populate_individual(individual);
        }
    } else {
        return NULL;
    }
    
    prop_val_t *ip_value = sslog_ss_get_property(individual, PROPERTY_IP);
    
    if(ip_value == NULL) {
        return NULL;
    }
    
    return (*env)->NewStringUTF(env, (char *)ip_value->prop_value);
}

/**
 * @brief Extracts Discussion service IP address
 *
 * @return IP address of the Discussion service if success, NULL otherwise
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getDiscussionServiceIP(
                                                                                        JNIEnv *env, jclass clazz){
    
    list_t *list = sslog_ss_get_individual_by_class_all(CLASS_DISCUSSIONSERVICE);
    individual_t *individual;
    
    if(list != NULL) {
        list_head_t* pos = NULL;
        list_for_each(pos, &list->links) {
            list_t* node = list_entry(pos, list_t, links);
            individual = (individual_t*)(node->data);
            sslog_ss_populate_individual(individual);
        }
    } else {
        return NULL;
    }
    
    prop_val_t *ip_value = sslog_ss_get_property(individual, PROPERTY_HASCLIENTURL);
    
    if(ip_value == NULL) {
        return NULL;
    }
    
    return (*env)->NewStringUTF(env, (char *)ip_value->prop_value);
}


/**
 * @brief Extracts microphone-service port
 *
 * @return Port in success and NULL otherwise
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getMicServicePort
(JNIEnv *env, jclass clazz) {
    
    list_t *list = sslog_ss_get_individual_by_class_all(CLASS_MICROPHONESERVICE);
    individual_t *individual;
    
    if(list != NULL) {
        list_head_t* pos = NULL;
        list_for_each(pos, &list->links) {
            list_t* node = list_entry(pos, list_t, links);
            individual = (individual_t*)(node->data);
            sslog_ss_populate_individual(individual);
        }
    } else {
        return NULL;
    }
    
    prop_val_t *port_value = sslog_ss_get_property(individual, PROPERTY_PORT);
    
    if(port_value == NULL) {
        return NULL;
    }
    
    return (*env)->NewStringUTF(env, (char *)port_value->prop_value);
}


/**
 * @brief Gets current speaker name
 *
 * @return Speaker name in success and NULL otherwise
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getSpeakerName(
                                                                                JNIEnv *env, jclass clazz) {
    
    prop_val_t *curTimeslotProp = sslog_ss_get_property(getCurrentSection(),
                                                        PROPERTY_CURRENTTIMESLOT);
    
    if(curTimeslotProp == NULL) {
        return NULL;
    }
    
    individual_t *curTimeslot = (individual_t *)curTimeslotProp->prop_value;
    prop_val_t *personLinkProp = sslog_ss_get_property(curTimeslot,
                                                       PROPERTY_TIMESLOTPERSON);
    
    if(personLinkProp == NULL) {
        return NULL;
    }
    
    individual_t *person = (individual_t *)personLinkProp->prop_value;
    prop_val_t *personName = sslog_ss_get_property(person, PROPERTY_NAME);
    
    if(personName != NULL) {
        return (*env)->NewStringUTF(env, (char *)personName->prop_value);
    } else {
        return NULL;
    }
}



/**
 * @brief Gets presentation URL
 *
 * @param index - index of time slot
 * @return Presentation URL in success and NULL otherwise
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getPresentationLink(
                                                                                     JNIEnv *env, jclass clazz, jint index) {
    
    individual_t *person = NULL;
    individual_t *presentation = NULL;
    individual_t *pTimeslot = NULL;
    
    pTimeslot = getTimeslot(index);
    
    if(pTimeslot == NULL)
        return NULL;
    
    prop_val_t *propPerson = sslog_ss_get_property(pTimeslot,
                                                   PROPERTY_TIMESLOTPERSON);
    
    if(propPerson != NULL) {
        person = (individual_t *) propPerson->prop_value;
    } else {
        return NULL;
    }
    
    prop_val_t *propPresents = sslog_ss_get_property(person,
                                                     PROPERTY_HASPRESENTATION);
    
    if(propPresents != NULL) {
        presentation = (individual_t *) propPresents->prop_value;
    } else {
        return NULL;
    }
    
    if(presentation != NULL) {
        prop_val_t *link = sslog_ss_get_property(presentation,
                                                 PROPERTY_PRESENTATIONURL);
        
        if(link != NULL) {
            return (*env)->NewStringUTF(env, (char *)link->prop_value);
        }
    }
    
    return NULL;
}

/**
 * @brief Gets person uuid
 *
 * @return Person uuid in success and NULL otherwise
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getPersonUuid
(JNIEnv *env, jclass clazz) {
    
    prop_val_t *person_prop = sslog_ss_get_property(personProfile,
                                                    PROPERTY_PERSONINFORMATION);
    individual_t *person;
    
    if(person_prop == NULL) {
        return NULL;
    }
    
    person = (individual_t *)person_prop->prop_value;
    
    if(person == NULL) {
        return NULL;
    }
    
    return (*env)->NewStringUTF(env, (char *)person->uuid);
}


/**
 * @brief Generates uuid
 *
 * @param uuid - initial uuid value
 * @return Generated uuid
 */
char* generateUuid(char *uuid) {
    
    int rand_val = 0, rand_length = 1, i = 0, postfix_length = 4;
    char *result = (char*) malloc (
                                   sizeof(char) * strlen(uuid) + postfix_length + 2);
    
    for(; i < postfix_length; rand_length *= 10, i++);
    
    do {
        srand(time(NULL));
        rand_val = rand() % rand_length;
        sprintf(result, "%s-%d", uuid, rand_val);
    } while(sslog_ss_exists_uuid(result) == 1);
    
    return result;
}



/**
 * @brief Extracts content-service URL
 *
 * @return Content service URL in success and NULL otherwise
 */
JNIEXPORT jstring JNICALL Java_petrsu_smartroom_android_srcli_KP_getContentUrl(
                                                                               JNIEnv *env, jclass clazz) {
    individual_t *contentService = getContentService();
    prop_val_t *urlProp = sslog_ss_get_property(contentService,
                                                PROPERTY_CONTENTURL);
    
    if(urlProp != NULL) {
        return (*env)->NewStringUTF(env, (char *)urlProp->prop_value);
    }
    
    return NULL;
}