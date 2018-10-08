package com.ford.evsmartcharge;

        import android.app.Activity;
        import android.content.Context;
        import android.content.Intent;
        import android.content.SharedPreferences;
        import android.os.AsyncTask;
        import android.os.Bundle;
        import android.support.annotation.Nullable;
        import android.support.v4.app.Fragment;
        import android.support.v7.app.ActionBar;
        import android.support.v7.app.ActionBar;
        //import android.support.v7.app.ActionBarActivity;
        import android.support.v7.app.AppCompatActivity;
        import android.support.v7.preference.PreferenceManager;
        import android.util.Log;
        import android.view.LayoutInflater;
        import android.view.View;
        import android.view.ViewGroup;
        import android.widget.Button;
        import android.widget.EditText;
        import android.widget.SeekBar;
        import android.widget.TextView;
        import android.widget.TimePicker;
        import android.content.SharedPreferences;
        import android.os.Bundle;
        import android.support.design.widget.FloatingActionButton;
        import android.support.design.widget.Snackbar;
        import android.support.v4.app.Fragment;
        import android.support.v4.app.FragmentTransaction;
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




        import java.io.PrintWriter;
        import java.net.Socket;
        import java.text.DecimalFormat;

public class ProfLogin extends AppCompatActivity {
    public String avalue;
    private SeekBar mSeekBar;
    private TextView mChargeText, ed1;
    private TextView mFeedbackText;
    private TimePicker mTimePicker;
    private Button mButton;
    private Context welcom;
    private Intent login, login2;
    private EditText username;
    private SharedPreferences mPref;
    private SharedPreferences.Editor mPrefEdit;


    Button Login;


    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.prof_login);
        ActionBar actionbar = getSupportActionBar();
        assert actionbar != null;
        actionbar.setDisplayHomeAsUpEnabled(true);
        actionbar.setHomeAsUpIndicator(R.drawable.ic_menu_slideshow);

        ed1 = (TextView) findViewById(R.id.ed1);
        login2 = getIntent();
        Bundle a = login2.getExtras();
        avalue = (String) a.get("member");
        ed1.setText(avalue);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                // app icon in action bar clicked; go home
                onBackPressed();
                return true;
            default:
                return super.onOptionsItemSelected(item);

        }
    }
}



//public class ProfLogin extends Activity {
  //  private SeekBar mSeekBar;
    //private TextView mChargeText;
    //private TextView mFeedbackText;
    //private TimePicker mTimePicker;
    //private Button mButton, Login;
    //private EditText username, ed1;
    //private SharedPreferences mPref;
    //private SharedPreferences.Editor mPrefEdit;

    //@Nullable
    //@Override
    //public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
    //returning our layout file
    //mPref = PreferenceManager.getDefaultSharedPreferences(getActivity());
    //mPrefEdit = mPref.edit();

    //return inflater.inflate(R.layout.prof_login, container, false);
    // }
    //protected void onCreate(Bundle savedInstanceState) {
      //  super.onCreate(savedInstanceState);
        //setContentView(R.layout.dialog_signin);
        //Login = (Button) findViewById(R.id.Login);
       // username = (EditText) findViewById(R.id.username);

        //Login.setOnClickListener(new View.OnClickListener() {
          //  @Override
            //public void onClick(View view) {
              //  if (view == Login) {
                //    String avalue = username.getText().toString();
                  //  ed1.setText(avalue);
//
  //              }
    //        }
      //  });
    //}
//}
