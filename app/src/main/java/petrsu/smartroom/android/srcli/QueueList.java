package petrsu.smartroom.android.srcli;

import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.app.ListActivity;
import android.widget.Button;
import android.widget.ListView;
import android.widget.RelativeLayout;

import com.mikepenz.iconics.typeface.FontAwesome;
import com.mikepenz.materialdrawer.Drawer;
import com.mikepenz.materialdrawer.DrawerBuilder;
import com.mikepenz.materialdrawer.model.DividerDrawerItem;
import com.mikepenz.materialdrawer.model.PrimaryDrawerItem;
import com.mikepenz.materialdrawer.model.SecondaryDrawerItem;
import com.mikepenz.materialdrawer.model.SectionDrawerItem;
import com.mikepenz.materialdrawer.model.interfaces.IDrawerItem;

import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.common.api.GoogleApiClient;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * Created by user on 14.05.16.
 */
public class QueueList extends ActionBarActivity {
    private ListView qlistView;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.queuelist);


        if (KP.chSpeaker) KP.deleteRequest(KP.gettingUsername);

        qlistView = (ListView) findViewById(R.id.qlistView);

        List <String> q = new ArrayList<String>();


        for (int x = 0; x < KP.getRequestCount(); x = x + 1) {
            q.add(KP.getRequestList(x));
            System.out.println(KP.getRequestList(x));
        }
        Subscription sub;
        sub = new Subscription();
        sub.execute("name1","name2","name3");   //первый тип

        ArrayAdapter <String> arr = new ArrayAdapter<String>(this, R.layout.listitem, R.id.label, q);
        qlistView.setAdapter(arr);


        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        try {
            setSupportActionBar(toolbar);
            if(getSupportActionBar() != null)
                getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        } catch(NullPointerException e){
            e.printStackTrace();
        }

        new DrawerBuilder()
                .withActivity(this)
                .withToolbar(toolbar)
                .withActionBarDrawerToggle(true)
                .withHeader(R.layout.drawer_header)
                .withDrawerWidthDp(320)
                .addDrawerItems(
                        new SectionDrawerItem().withName(R.string.services),
                        new PrimaryDrawerItem().withName(R.string.agenda).withIcon(FontAwesome.Icon.faw_server),
                        new PrimaryDrawerItem().withName(R.string.presentation).withIcon(FontAwesome.Icon.faw_image),
                        new PrimaryDrawerItem().withName("SocialProgram").withIcon(FontAwesome.Icon.faw_globe),
                        new PrimaryDrawerItem().withName("QueueActivity").withIcon(FontAwesome.Icon.faw_globe),
                        new PrimaryDrawerItem().withName("QueueList").withIcon(FontAwesome.Icon.faw_globe),

                        new SectionDrawerItem().withName(R.string.discussion),
                        new PrimaryDrawerItem().withName(R.string.discussionCur).withIcon(FontAwesome.Icon.faw_comment_o),
                        new PrimaryDrawerItem().withName(R.string.discussionList).withIcon(FontAwesome.Icon.faw_comments_o),

                        new SectionDrawerItem().withName(R.string.action_settings),
                        new PrimaryDrawerItem().withName(R.string.action_settings).withIcon(FontAwesome.Icon.faw_cog),

                        new SectionDrawerItem().withName(R.string.help),
                        new PrimaryDrawerItem().withName(R.string.manual).withIcon(FontAwesome.Icon.faw_download),

                        new DividerDrawerItem(),
                        new SecondaryDrawerItem().withName(R.string.exitClientTitle).withIcon(FontAwesome.Icon.faw_close)
                ).withOnDrawerItemClickListener(new Drawer.OnDrawerItemClickListener() {
            @Override
            public boolean onItemClick(AdapterView<?> parent, View view, int position, long id, IDrawerItem drawerItem) {
                //Toast.makeText(Agenda.this, String.valueOf(id), Toast.LENGTH_SHORT).show();
                switch ((int) id) {
                    case 1:startActivity(Navigation.getAgendaIntent(getApplicationContext()));        break;
                    case 2:startActivity(Navigation.getPresentationIntent(getApplicationContext()));  break;
                    case 3:startActivity(Navigation.getSocialProgramIntent(getApplicationContext())); break;
                    case 4:startActivity(Navigation.getQueueActIntent(getApplicationContext()));      break;
                    case 5:                                                                           break;
                    case 7:startActivity(Navigation.getCurDisqIntent(getApplicationContext()));       break;
                    case 8:startActivity(Navigation.getDisqListIntent(getApplicationContext()));      break;
                    case 10:startActivity(Navigation.getSettingsIntent(getApplicationContext()));     break;
                    case 12:startActivity(Navigation.getManIntent(getApplicationContext()));          break;
                    case 14:startActivity(Navigation.exitApp());                                      break;
                    default:                                                                          break;
                }
                return true;
            }
        }).build();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.

    }
}


class Subscription extends AsyncTask<String,Integer,Void> {

    @Override
    protected  void onPreExecute() {
        super.onPreExecute();
        System.out.println("BEGIN");
    }

    @Override
    protected Void doInBackground(String...names){
        try {
            int cnt = 0;
            for (String name : names) {
                showName(name);
                publishProgress(++cnt);     //выводим промежуточный результат (вызов onProgressUpdate)
                                            //второй тип
            }
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e){
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected  void  onProgressUpdate(Integer...values){
        super.onProgressUpdate(values);
        System.out.println("***"+values[0]+"***");
    }

    @Override
    protected  void  onPostExecute(Void result) {
        super.onPostExecute(result);
        System.out.println("END");
    }

    private void showName(String name) throws InterruptedException{
        TimeUnit.SECONDS.sleep(2);
    }
}