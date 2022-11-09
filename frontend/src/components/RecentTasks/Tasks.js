import React from "react";
import Task from "./Task";


export default function Tasks(props) {
    return (
        <div>
        {props.tasks.map((task, number) => 
            <div data-testid={"task-" + number.toString()} key={number.toString()}>
                <Task
                    key={number.toString()}
                    title={task.title}
                    time={task.time.replace('T', ' ').split('.')[0]}
                    image={task.receiver_user.image}
                    status={task.status}
                    id={task.id}
                />
            </div>)}
            <hr className="border-gray-300" />
            <div className="mt-5 text-center py-2">
                <a href="" className="text-lg text-gray-500 hover:text-gray-400">Посмотреть всю историю</a>
            </div>
        </div>
    );
};