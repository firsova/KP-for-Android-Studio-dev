package petrsu.smartroom.android.srcli;

import android.content.Intent;
import android.graphics.Bitmap;
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

/**
 * Created by user on 11.05.16.
 */
public class QueueActivity  extends ActionBarActivity implements View.OnClickListener {
    private Button toQueue;
    private Button exitQueue;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.queueserv);

        toQueue = (Button) findViewById (R.id.toQueue);
        toQueue.setOnClickListener(this);
        exitQueue = (Button) findViewById (R.id.exitQueue);
        exitQueue.setOnClickListener(this);

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

                        new SectionDrawerItem().withName(R.string.discussion),
                        new PrimaryDrawerItem().withName(R.string.discussionCur).withIcon(FontAwesome.Icon.faw_comment_o),
                        new PrimaryDrawerItem().withName(R.string.discussionList).withIcon(FontAwesome.Icon.faw_comments_o),

                        new SectionDrawerItem().withName(R.string.action_settings),
                        new PrimaryDrawerItem().withName(R.string.action_settings).withIcon(FontAwesome.Icon.faw_cog),

                        new SectionDrawerItem().withName(R.string.help),
                        new PrimaryDrawerItem().withName(R.string.manual).withIcon(FontAwesome.Icon.faw_download),

                        new DividerDrawerItem(),
                        new SecondaryDrawerItem().withName(R.string.exitClientTitle).withIcon(FontAwesome.Icon.faw_close),
                        new PrimaryDrawerItem().withName("QueueActivity").withIcon(FontAwesome.Icon.faw_globe)
                ).withOnDrawerItemClickListener(new Drawer.OnDrawerItemClickListener() {
            @Override
            public boolean onItemClick(AdapterView<?> parent, View view, int position, long id, IDrawerItem drawerItem) {
                //Toast.makeText(Agenda.this, String.valueOf(id), Toast.LENGTH_SHORT).show();
                switch ((int) id) {
                    case 1: startActivity(Navigation.getAgendaIntent(getApplicationContext()));     break;
                    case 2:
                        startActivity(Navigation.getPresentationIntent(getApplicationContext()));   break;
                    case 3:
                        startActivity(Navigation.getSocialProgramIntent(getApplicationContext()));  break;
                    case 5:
                        startActivity(Navigation.getCurDisqIntent(getApplicationContext()));        break;
                    case 6:
                        startActivity(Navigation.getDisqListIntent(getApplicationContext()));       break;
                    case 8:
                        startActivity(Navigation.getSettingsIntent(getApplicationContext()));       break;
                    case 10:
                        startActivity(Navigation.getManIntent(getApplicationContext()));            break;
                    case 12:
                        startActivity(Navigation.exitApp());                                        break;
                    case 13:                                                                        break;
                    default:                                                                        break;
                }
                return true;
            }
        }).build();
    }

    public void onClick(View v){

        switch(v.getId()) {

			/* toQueue button */
            case R.id.toQueue:

                break;

			/* exitQueue button */
            case R.id.exitQueue:

                break;
        }
    }
}
