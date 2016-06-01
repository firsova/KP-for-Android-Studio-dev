package petrsu.smartroom.android.srcli;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;



public class QueueService extends Service{

    public static CharSequence[] titleArray;


    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }


    @Override
    public void onStart(Intent intent, int startId) {


    }

    public static void createRequest() {

        if (KP.existingRequest(KP.gettingUsername) == 0)
        {
                System.out.println("Такого реквеста еще не было");
                System.out.println(KP.registerRequest(KP.gettingUsername, "SENDED"));
        }
                else {
                    System.out.println("Такой реквест уже был");
        }
    }


    public static void deleteRequest() {

        if (KP.existingRequest(KP.gettingUsername) == 0)
        {
            System.out.println("Данный пользователь еще не посылал реквест");
        }
        else {
            System.out.println("Реквест от данного пользователя удален");
            System.out.println(KP.deleteRequest(KP.gettingUsername));

        }
    }

}


