package petrsu.smartroom.android.srcli;

import android.app.Activity;
import android.app.Service;
import android.content.ComponentName;
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

     static int createRequest() {

        if (KP.existingRequest(KP.gettingUsername) == 0)
        {

            System.out.print("\nREQUEST-INFO: Такого реквеста еще не было: "+ KP.registerRequest(KP.gettingUsername, "SENDED"));
            //startService(new Intent(this, QueueList.class));
            return 0;

        }
                else {
                    System.out.print("\nREQUEST-INFO: Такой реквест уже был");
                    return -1;
        }
    }


    public static int deleteRequest() {

        if (KP.existingRequest(KP.gettingUsername) == 0)
        {
            System.out.print("\nREQUEST-INFO: Данный пользователь еще не посылал реквест");
            return 0;
        }
        else {
            System.out.print("\nREQUEST-INFO: Реквест от данного пользователя удален: "+KP.deleteRequest(KP.gettingUsername));
            return -1;

        }
    }

}


