package project.project;

import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.firebase.ui.database.FirebaseRecyclerAdapter;
import com.firebase.ui.database.FirebaseRecyclerOptions;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ServerValue;
import com.google.firebase.database.ValueEventListener;

import java.lang.reflect.Member;

public class MainActivity extends AppCompatActivity {

    RecyclerView Mrecyclerview;
    FirebaseDatabase database;
    DatabaseReference reference;
    LinearLayoutManager linearLayoutManager;
    String name;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Mrecyclerview = findViewById(R.id.recyclerview_video);
        Mrecyclerview.setHasFixedSize(true);
        linearLayoutManager = new LinearLayoutManager(this);
        Mrecyclerview.setLayoutManager(linearLayoutManager);
        linearLayoutManager.setReverseLayout(true);
        linearLayoutManager.setStackFromEnd(true);
        database = FirebaseDatabase.getInstance();
        reference = database.getReference("video");

        //reference.orderByChild("timestamp").limitToLast(10);

    }
    @Override
    protected void onStart() {
        super.onStart();
        FirebaseRecyclerOptions<member> options =
                new FirebaseRecyclerOptions.Builder<member> ()
                        .setQuery(reference, member.class)
                        .build();
        FirebaseRecyclerAdapter<member, ViewHolder> firebaseRecyclerAdapter =
                new FirebaseRecyclerAdapter<member, ViewHolder>(options) {
                    @NonNull
                    @Override
                    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
                        View view = LayoutInflater.from(parent.getContext())
                                .inflate(R.layout.row, parent, false);
                        return new ViewHolder(view);
                    }
                    @Override
                    protected void onBindViewHolder(@NonNull ViewHolder holder, int position, @NonNull member model) {
                        holder.setVideo(getApplication(), model.getTitle(), model.getUrl());
                        holder.setOnClickListener(new ViewHolder.ClickListener() {
                            @Override
                            public void onItemClick(View view, int position) {

                            }
                            @Override
                            public void onItemLongClick(View view, int position) {
                                name = getItem(position).getTitle();
                                showDeleteDialog(name);
                            }
                        });
                    }
        };
        firebaseRecyclerAdapter.startListening();
        Mrecyclerview.setAdapter(firebaseRecyclerAdapter);
    }

    private void showDeleteDialog(String title) {
        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
        builder.setTitle("Delete");
        builder.setMessage("Are you sure to delete this video?");
        builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                Query query = reference.orderByChild("title").equalTo(title);
                query.addListenerForSingleValueEvent(new ValueEventListener() {
                    @Override
                    public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                        for (DataSnapshot dataSnapshot1 : dataSnapshot.getChildren()) {
                            dataSnapshot1.getRef().removeValue();
                        }
                        Toast.makeText(MainActivity.this, "Video deleted successfully.", Toast.LENGTH_SHORT).show();
                    }

                    @Override
                    public void onCancelled(@NonNull DatabaseError databaseError) {

                    }
                });
            }
        });
        builder.setNegativeButton("No", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                dialogInterface.dismiss();
            }
        });
        AlertDialog alertDialog = builder.create();
        alertDialog.show();
    }
}