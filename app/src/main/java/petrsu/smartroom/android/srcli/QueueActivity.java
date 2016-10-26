package petrsu.smartroom.android.srcli;

import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
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


/**
 * Created by user on 11.05.16.
 */
public class QueueActivity extends ActionBarActivity implements View.OnClickListener {
    private Button toQueue;
    private Button exitQueue;
    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    private GoogleApiClient client;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.queueserv);

        toQueue = (Button) findViewById(R.id.toQueue);
        toQueue.setOnClickListener(this);
        exitQueue = (Button) findViewById(R.id.exitQueue);
        exitQueue.setOnClickListener(this);

        if (QueueService.createRequest() == 0)
        {
            exitQueue.setBackgroundColor(getResources().getColor(R.color.gray));
            QueueService.deleteRequest();
        } else {
            toQueue.setBackgroundColor(getResources().getColor(R.color.gray));
        }

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
                        new PrimaryDrawerItem().withName("QueueActivity").withIcon(FontAwesome.Icon.faw_globe),
                        new PrimaryDrawerItem().withName("QueueList").withIcon(FontAwesome.Icon.faw_globe),

                        new DividerDrawerItem(),
                        new SecondaryDrawerItem().withName(R.string.exitClientTitle).withIcon(FontAwesome.Icon.faw_close)
                ).withOnDrawerItemClickListener(new Drawer.OnDrawerItemClickListener() {
            @Override
            public boolean onItemClick(AdapterView<?> parent, View view, int position, long id, IDrawerItem drawerItem) {
                //Toast.makeText(Agenda.this, String.valueOf(id), Toast.LENGTH_SHORT).show();
                switch ((int) id) {
                    case 1: break;
                    case 2:
                        startActivity(Navigation.getQueueActListIntent(getApplicationContext()));   break;
                    case 4:
                        startActivity(Navigation.exitApp());                                        break;
                    default:                                                                        break;
                }
                return true;
            }
        }).build();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();
    }

    public void onClick(View v) {

        switch (v.getId()) {

			/* toQueue button */
            case R.id.toQueue:

                QueueService queue1;
                queue1 = new QueueService();

                queue1.createRequest();

                toQueue.setBackgroundColor(getResources().getColor(R.color.gray));
                exitQueue.setBackgroundColor(getResources().getColor(R.color.md_red_A400));
                break;

			/* exitQueue button */
            case R.id.exitQueue:

                QueueService queue2;
                queue2 = new QueueService();

                queue2.deleteRequest();


                exitQueue.setBackgroundColor(getResources().getColor(R.color.gray));
                toQueue.setBackgroundColor(getResources().getColor(R.color.md_light_green_A700));

                break;
        }
    }

    @Override
    public void onStart() {
        super.onStart();


        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Queue Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app deep link URI is correct.
                Uri.parse("android-app://petrsu.smartroom.android.srcli/http/host/path")
        );
        AppIndex.AppIndexApi.start(client, viewAction);


        //    if (KP.headChanged(KP.gettingUsername) == 0)
       //     {
               // startService(new Intent(getApplicationContext(), MicActivity.class));
               // System.out.println("Здесь включается микрофон");

        //    }


    }

    @Override
    public void onStop() {
        super.onStop();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Queue Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app deep link URI is correct.
                Uri.parse("android-app://petrsu.smartroom.android.srcli/http/host/path")
        );
        AppIndex.AppIndexApi.end(client, viewAction);
        client.disconnect();
    }
}
