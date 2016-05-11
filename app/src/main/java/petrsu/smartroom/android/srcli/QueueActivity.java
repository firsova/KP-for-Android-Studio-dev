package petrsu.smartroom.android.srcli;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;
import android.widget.RelativeLayout;

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
