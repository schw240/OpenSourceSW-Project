package com.example.warnings;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.ContactsContract;
import android.provider.MediaStore;
import android.renderscript.ScriptGroup;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {
    public ImageView iv;
    public String host = "192.168.0.2";
    public int port = 9955;
    public Socket socket;
    public Handler mHandler;
    public Handler m2Handler;

    public DataOutputStream dos;
    //    private DataInputStream dis;
    public InputStream in;

    public BufferedInputStream bis;

//    public static Bitmap bitmap;




    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        checkSelfPermission();
        iv = findViewById(R.id.browse);
        iv.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                Intent intent = new Intent();
                //기기 기본 갤러리 접근
                intent.setType(MediaStore.Images.Media.CONTENT_TYPE);
                // 구글 갤러리 접근
                // intent.setType("image/*");
                intent.setAction(Intent.ACTION_GET_CONTENT);
                startActivityForResult(intent,101);
            }
        });
    }
    // 권한에 대한 응답이 있을때 작동하는 함수
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        // 권한을 허용 했을 경우
        if(requestCode == 1) {
            int length = permissions.length;
            for (int i = 0; i < length; i++) {
                if (grantResults[i] == PackageManager.PERMISSION_GRANTED) {
                    // 동의
                    Log.d("MainActivity", "권한 허용 : " + permissions[i]);
                }
            }
        }
    }
    public void checkSelfPermission() {
        String temp = "";
        //파일 읽기 권한 확인
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            temp += Manifest.permission.READ_EXTERNAL_STORAGE + " ";
        } //파일 쓰기 권한 확인
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            temp += Manifest.permission.WRITE_EXTERNAL_STORAGE + " ";
        }
        if (TextUtils.isEmpty(temp) == false) {
            // 권한 요청
            ActivityCompat.requestPermissions(this, temp.trim().split(" "), 1);
        } else {
            // 모두 허용 상태
            Toast.makeText(this, "권한을 모두 허용", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 101 && resultCode == RESULT_OK) {
            try {
                InputStream is = getContentResolver().openInputStream(data.getData());
                final Bitmap bitmap = BitmapFactory.decodeStream(is);
                connect(bitmap);
                is.close();
                      //       iv.setImageBitmap(bitmap);

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        else if (requestCode == 101 && resultCode == RESULT_CANCELED) {
            Toast.makeText(this, "취소", Toast.LENGTH_SHORT).show();
        }
    }

    void connect(final Bitmap bitmap){
        mHandler = new Handler();
        Log.w("connect","연결 하는중");
        // 받아오는거
        Thread checkUpdate = new Thread() {
            public void run() {
                //            InputStream in =null;
                try {
                    socket = new Socket(host, port);
                    Log.w("서버 접속됨", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버접속못함");
                    e1.printStackTrace();
                }
                Log.w("edit 넘어가야 할 값 : ","안드로이드에서 서버로 연결요청");
                try {
                    dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    //                dis = new DataInputStream(socket.getInputStream());  // input에 받을꺼 넣어짐
                    in =  socket.getInputStream();
                    bis = new BufferedInputStream(in);

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }

                Log.w("버퍼","버퍼생성 잘됨");

                try {
                    while(true) {
                        ByteArrayOutputStream bout = new ByteArrayOutputStream();

                        bitmap.compress(Bitmap.CompressFormat.PNG,80,bout);

                        dos.write(bout.toByteArray());


                        // InputStream in = socket.getInputStream();
                        Bitmap bm = BitmapFactory.decodeStream(bis);

                        iv.setImageBitmap(bm);





                    }
                }catch (Exception e){
                    setContentView(R.layout.activity_main);
                }
            }
        };checkUpdate.start();
    }
}


