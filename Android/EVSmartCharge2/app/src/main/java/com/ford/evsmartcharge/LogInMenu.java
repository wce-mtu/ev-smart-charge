package com.ford.evsmartcharge;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.app.FragmentTransaction;
import android.content.Context;
import android.os.Bundle;
import android.content.Intent;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.preference.PreferenceManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.support.v7.app.ActionBar;
//import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.AppCompatDelegate;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.TimePicker;
import android.support.v7.preference.PreferenceManager;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.io.PrintWriter;
import java.net.Socket;
import java.text.DecimalFormat;

public class LogInMenu extends AppCompatActivity{
    public String avalue, bvalue;
    private SeekBar mSeekBar;
    private TextView mChargeText;
    private TextView mFeedbackText;
    private TimePicker mTimePicker;
    private Button mButton, Login, Cancel;
    private Context welcom;
    private Fragment Home;
    private FragmentTransaction FT;
    private Intent login, cancel, login2;
    private EditText username, password, ed1;
    private SharedPreferences mPref;
    private SharedPreferences.Editor mPrefEdit;
    private DatabaseReference mDatabase;

    @Nullable

    //login profile page
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.dialog_signin);
        ActionBar actionbar = getSupportActionBar();
        assert actionbar != null;
        actionbar.setDisplayHomeAsUpEnabled(true);
        actionbar.setHomeAsUpIndicator(R.drawable.ic_menu_slideshow);

        // Screen Components
        Login = (Button) findViewById(R.id.Login);
        username = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);
        //FT = getFragmentManager().beginTransaction();

        Login.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                if (v == Login) {
                    avalue = username.getText().toString();
                    bvalue = password.getText().toString();
                    login = new Intent(LogInMenu.this, ProfLogin.class);

                    // Get Firebase reference
                    mDatabase = FirebaseDatabase.getInstance().getReference();

                    // Write username and password to database
                    mDatabase.child("users").child(avalue).setValue(bvalue);
                }
                // else if (Cancel != null){
                //   this.finish();

                // private void displaySelectedScreen(int itemId) {
                //Fragment fragment = null;
                // }
                // switch (itemId) {
                //case R.id.Cancel:
                //fragment = new HomeMenu();
                // break;
                // }

                //login2 = new Intent(LogInMenu.this, getApplicationContext().getClass());
                //startActivity(login2);
            }
        });


    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android. R.id.home:
                // app icon in action bar clicked; go home
                onBackPressed();
                return true;
            default:
                return super.onOptionsItemSelected(item);

        }
    }
}