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
import android.widget.ImageButton;
import android.widget.RelativeLayout;
import android.util.Log;
import android.view.MotionEvent;
import android.app.usage.UsageEvents;
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

public class MicActivity extends ActionBarActivity implements View.OnTouchListener {
    private ImageButton micButton;
    private Button exitBtn;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.micactivity);

        micButton = (ImageButton) findViewById(R.id.micButton);
        micButton.setOnTouchListener(this);

        exitBtn = (Button) findViewById(R.id.exitButton);
        exitBtn.setOnTouchListener(this);

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        try {
            setSupportActionBar(toolbar);
            if (getSupportActionBar() != null)
                getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        } catch (NullPointerException e) {
            e.printStackTrace();
        }

        new DrawerBuilder()
                .withActivity(this)
                .withToolbar(toolbar)
                .withActionBarDrawerToggle(true)
                .withHeader(R.layout.drawer_header)
                .withDrawerWidthDp(320)
                .addDrawerItems(
                        new SecondaryDrawerItem().withName(R.string.exitClientTitle).withIcon(FontAwesome.Icon.faw_close)
                ).withOnDrawerItemClickListener(new Drawer.OnDrawerItemClickListener() {
            @Override
            public boolean onItemClick(AdapterView<?> parent, View view, int position, long id, IDrawerItem drawerItem) {
                //Toast.makeText(Agenda.this, String.valueOf(id), Toast.LENGTH_SHORT).show();
                switch ((int) id) {
                    case 0:
                        startActivity(Navigation.exitApp());                                        break;
                    default:                                                                        break;
                }
                return true;
            }
        }).build();
    }


    @Override
    public boolean onTouch(View view, MotionEvent motionEvent) {
        switch (view.getId()) {
            case R.id.micButton: {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN) {
                    //startService(new Intent(this, MicService.class));
                    Log.i("Ontouch:", "case mic, event down");
                    break;
                }
                if (motionEvent.getAction() == MotionEvent.ACTION_UP) {
                    //stopService(new Intent(this, MicService.class));
                    Log.i("Ontouch:", "case mic, event up");
                    break;
                }
            }
            case R.id.exitButton: {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN) {
                    startActivity(Navigation.getQueueActListIntent(this));
                    System.out.println("\nУдаляем HEAD: "+KP.deleteRequest(KP.gettingUsername));
                    break;
                }
            }
        }
        return false;
    }
}