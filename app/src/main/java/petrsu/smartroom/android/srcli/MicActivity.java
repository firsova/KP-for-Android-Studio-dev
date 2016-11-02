package petrsu.smartroom.android.srcli;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ImageButton;
import android.util.Log;
import android.view.MotionEvent;
import android.widget.Toast;

import com.mikepenz.iconics.typeface.FontAwesome;
import com.mikepenz.materialdrawer.Drawer;
import com.mikepenz.materialdrawer.DrawerBuilder;
import com.mikepenz.materialdrawer.model.SecondaryDrawerItem;
import com.mikepenz.materialdrawer.model.interfaces.IDrawerItem;

public class MicActivity extends ActionBarActivity implements View.OnTouchListener {
    private ImageButton micButton;
    private Button exitBtn;
    public static boolean isMicServiceLaunched;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.micactivity);

        QueueActivity.isUserOnMicIntent = true;
        MicActivity.isMicServiceLaunched = true;

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
                    if (KP.existingRequest(KP.gettingUsername) == 1){
                         //startService(new Intent(this, MicService.class));
                        Log.i("Ontouch:", "case mic, event down");
                        break;
                    } else {
                        startActivity(Navigation.getQueueActListIntent(this));
                        Toast.makeText(this,KP.gettingUsername +" was deleted from list by chairman", Toast.LENGTH_SHORT).show();
                        break;
                    }
                }
                if (motionEvent.getAction() == MotionEvent.ACTION_UP) {
                    if (KP.existingRequest(KP.gettingUsername) == 1) {
                        //stopService(new Intent(this, MicService.class));
                        MicActivity.isMicServiceLaunched = false;
                        Log.i("Ontouch:", "case mic, event up");
                        break;
                    }else{
                        startActivity(Navigation.getQueueActListIntent(this));
                        Toast.makeText(this,KP.gettingUsername +" was deleted from list by chairman", Toast.LENGTH_SHORT).show();
                        break;
                    }
                }
            }
            case R.id.exitButton: {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN) {
                    startActivity(Navigation.getQueueActListIntent(this));
                    System.out.println("\nУдаляем HEAD: "+KP.deleteRequest(KP.gettingUsername));
                    QueueActivity.isUserOnMicIntent = false;

                    break;
                }
            }
        }
        return false;
    }
}