package petrsu.smartroom.android.srcli;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.app.ListActivity;
import android.widget.Button;
import android.widget.ListView;
import android.widget.RelativeLayout;
import android.widget.Toast;

import com.google.android.gms.common.server.converter.StringToIntConverter;
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
public class QueueList extends ActionBarActivity implements AdapterView.OnItemLongClickListener {

    public String headUsername;
    private ListView qlistView;
    ArrayAdapter <String> arr;
    List <String> q;

    void refresh(){
        q.clear();
       // arr.clear();
        for (int x = 0; x < KP.getRequestCount(); x = x + 1) {
            q.add(KP.getRequestList(x));
        }

        //arr.addAll(q);
        arr.notifyDataSetChanged();
        //qlistView.setAdapter(arr);
    }

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.queuelist);

        //если сменился выступающий
        //if (KP.chSpeaker) KP.deleteRequest(KP.gettingUsername);

        qlistView = (ListView) findViewById(R.id.qlistView);

        q = new ArrayList<>();

        qlistView.setAdapter(arr);
        qlistView.setOnItemLongClickListener(this);

        //q.clear();
        //arr.clear();

        for (int x = 0; x < KP.getRequestCount(); x = x + 1) {
            q.add(KP.getRequestList(x));
        }
        arr = new ArrayAdapter<String>(this, R.layout.listitem, R.id.label, q);
        //arr.addAll(q);
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
                        new PrimaryDrawerItem().withName("QueueActivity").withIcon(FontAwesome.Icon.faw_globe),
                        new PrimaryDrawerItem().withName("QueueList").withIcon(FontAwesome.Icon.faw_globe),

                        new DividerDrawerItem(),
                        new SecondaryDrawerItem().withName("Refresh").withIcon(FontAwesome.Icon.faw_refresh),
                        new SecondaryDrawerItem().withName(R.string.exitClientTitle).withIcon(FontAwesome.Icon.faw_close)
                ).withOnDrawerItemClickListener(new Drawer.OnDrawerItemClickListener() {
            @Override
            public boolean onItemClick(AdapterView<?> parent, View view, int position, long id, IDrawerItem drawerItem) {
                //Toast.makeText(Agenda.this, String.valueOf(id), Toast.LENGTH_SHORT).show();
                switch ((int) id) {
                    case 1: startActivity(Navigation.getQueueActIntent(getApplicationContext()));   break;
                    case 2: break;
                    case 4: refresh(); break;
                    case 5: startActivity(Navigation.exitApp());                                    break;
                    default:                                                                        break;
                }
                return true;
            }
        }).build();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.

    }


    @Override
    public boolean onItemLongClick(AdapterView<?> adapterView, View view, int pos, long id) {
        Toast.makeText(this, "Pressed on " + pos + " element", Toast.LENGTH_SHORT).show();
        String user = q.get(pos);
        Toast.makeText(this, "Pressed on " + user, Toast.LENGTH_SHORT).show();
        return false;
    }
}

