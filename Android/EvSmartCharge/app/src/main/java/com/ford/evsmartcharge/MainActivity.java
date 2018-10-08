package com.ford.evsmartcharge;

import android.content.res.Configuration;
import android.os.AsyncTask;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MenuItem;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.SeekBar;
import android.widget.TimePicker;
import android.widget.TextView;
import android.view.View;
import android.widget.ListView;

import java.io.*;
import java.net.*;

public class MainActivity extends AppCompatActivity {
    private TextView output_time;
    private TextView charge_pct;
    private TimePicker timePicker;
    private ListView mDrawerList;
    private DrawerLayout mDrawerLayout;
    private String mActivityTitle;
    private ActionBarDrawerToggle mDrawerToggle;
    private SeekBar mSeekBar;
    private ArrayAdapter<String> listAdapter;
    String fragmentArray[] = {"Home", "User Profile", "History"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        timePicker = (TimePicker) findViewById(R.id.timePicker);
        output_time = (TextView) findViewById(R.id.textView2);
        charge_pct = (TextView) findViewById(R.id.textView3);
        mDrawerList = (ListView) findViewById(R.id.navList);
        mDrawerLayout = (DrawerLayout)findViewById(R.id.activity_main);
        mActivityTitle = getTitle().toString();
        mSeekBar = (SeekBar) findViewById(R.id.seekBar);

        listAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, fragmentArray);
        mDrawerList.setAdapter(listAdapter);

        mDrawerList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Fragment fragment;

                switch (position) {
                    //home
                    case 0:
                        fragment = new ProfileFragment();
                        break;
                    case 1:
                        fragment = new ProfileFragment();
                        break;
                    default:
                        fragment = new ProfileFragment();
                        break;
                }

                FragmentManager fragmentManager = getSupportFragmentManager();
                fragmentManager.beginTransaction().replace(R.id.activity_main, fragment).commit();
            }

        });

        setupDrawer();

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeButtonEnabled(true);

        mSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                getRequestedCharge();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

    }

    public void setActionBarTitle(String title) {
        getSupportActionBar().setTitle(title);
    }

    public void getRequestedCharge()
    {
        int seekValue = mSeekBar.getProgress();
        String x = seekValue + "% Charge";
        charge_pct.setText(new StringBuilder(x));
    }

    private void setupDrawer() {
        mDrawerToggle = new ActionBarDrawerToggle(this, mDrawerLayout,
                        R.string.drawer_open, R.string.drawer_close) {

            /** Called when a drawer has settled in a completely open state. */
            public void onDrawerOpened(View drawerView) {
                super.onDrawerOpened(drawerView);
                getSupportActionBar().setTitle("Navigation");
                invalidateOptionsMenu(); // creates call to onPrepareOptionsMenu()
            }

            /** Called when a drawer has settled in a completely closed state. */
            public void onDrawerClosed(View view) {
                super.onDrawerClosed(view);
                getSupportActionBar().setTitle(mActivityTitle);
                invalidateOptionsMenu(); // creates call to onPrepareOptionsMenu()
            }
        };

        mDrawerToggle.setDrawerIndicatorEnabled(true);
        mDrawerLayout.addDrawerListener(mDrawerToggle);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        /*noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        } */

        // Activate the navigation drawer toggle
        if (mDrawerToggle.onOptionsItemSelected(item)) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onPostCreate(Bundle savedInstanceState) {
        super.onPostCreate(savedInstanceState);
        mDrawerToggle.syncState();
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        mDrawerToggle.onConfigurationChanged(newConfig);
    }

    public void setTime(View view) {
        int hour = timePicker.getHour();
        int min = timePicker.getMinute();
        int reqCharge = mSeekBar.getProgress();

        showTime(hour, min, reqCharge);
    }

    public void showTime(int hour, int min, int reqCharge) {
        String format;
        String zero = "";
        if (hour == 0) {
            hour += 12;
            format = "AM";
        } else if (hour == 12) {
            format = "PM";
        } else if (hour > 12) {
            hour -= 12;
            format = "PM";
        } else {
            format = "AM";
        }
        if(min < 10) {
            zero = "0";
        }

        new PostTask().execute(Integer.toString(hour), Integer.toString(min), zero, format,
                               Integer.toString(reqCharge));

        output_time.setText(new StringBuilder().append("Your car will be charged to ")
                            .append(reqCharge).append("% by ").append(hour).append(":")
                            .append(zero).append(min).append(" ").append(format));
    }

    public void sendData(int hour, int min) {
        Thread t = new Thread();
        
    }

    // The definition of our task class
    private class PostTask extends AsyncTask<String, Integer, String> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected String doInBackground(String... params) {
            String hour = params[0];
            String min = params[1];
            String zero = params[2];
            String format = params[3];
            String reqCharge = params[4];

            try {
                Socket soc = new Socket("141.219.217.133" , 8888);
                //DataOutputStream dataout = new DataOutputStream(soc.getOutputStream());
                PrintWriter out = new PrintWriter(soc.getOutputStream(), true);
                //dataout.writeChars(hour + " " + min + " " + format + " " + reqCharge);
                //dataout.writeInt(Integer.parseInt(min));
                //dataout.writeChars(format);
                //dataout.writeInt(Integer.parseInt(reqCharge));

                out.print(hour + " " + min + " " + format + " " + reqCharge);
                out.flush();
                //dataout.close();
                soc.close();
                return "Yayyyy";

            } catch(Exception e){
                e.printStackTrace();
                return "Noooo";
            }
        }

        @Override
        protected void onProgressUpdate(Integer... values) {
            super.onProgressUpdate(values);
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
        }
    }
}
