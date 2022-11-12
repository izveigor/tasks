import React from 'react';
import { USERS_URL_WITHOUT_SLASH } from '../../features/constants';


export default function Task(props) {
    return (
        <div>
            <hr className="border-gray-300" />
            <div className="mt-5 w-50 px-2 py-2 flex justify-center">
                <div className="ml-3 w-16 h-16">
                    <img data-testid="task-image-test" className="rounded-full align-middle" src={USERS_URL_WITHOUT_SLASH + props.image} />
                </div>
                <div className="grid md:grid-rows-2 grid-rows-3 ml-3">
                    <span data-testid="task-name-test" className="text-md md:row-span-1 row-span-2">{props.title} #{props.id}</span>
                    <span data-testid="task-time-test" className="text-sm text-gray-500">{props.time}</span>
                </div>
                {(props.status == "Успешно") && (<div className="ml-8 h-100">
                    <div className="align-middle inline-block">
                        <div className="bg-green-200 flex rounded-2xl w-100 px-2 py-1">
                            <div className="h-100">
                                <div className="animate-pulse inline-block align-middle rounded-full h-2 w-2 bg-green-600"></div>
                            </div>
                            <div className="h-100">
                                <p data-testid="task-status-test" className="ml-2 align-middle inline-block text-sm text-green-600 w-[5em]">Успешно</p>
                            </div>
                        </div>
                    </div>
                </div>)}
                {(props.status == "Обработка") && (<div className="ml-8 h-100">
                    <div className="align-middle inline-block">
                        <div className="bg-orange-200 flex rounded-2xl w-100 px-2 py-1">
                            <div className="h-100">
                                <div className="animate-pulse inline-block align-middle rounded-full h-2 w-2 bg-orange-600"></div>
                            </div>
                            <div className="h-100">
                                <p data-testid="task-status-test" className="ml-2 align-middle inline-block text-sm text-orange-600 w-[5em]">Обработка</p>
                            </div>
                        </div>
                    </div>
                </div>)}
                {(props.status == "Закрыто") && (<div className="ml-8 h-100">
                    <div className="align-middle inline-block">
                        <div className="bg-red-200 flex rounded-2xl w-100 px-2 py-1">
                            <div className="h-100">
                                <div className="animate-pulse inline-block align-middle rounded-full h-2 w-2 bg-red-600"></div>
                            </div>
                            <div className="h-100">
                                <p data-testid="task-status-test" className="ml-2 align-middle inline-block text-sm text-red-600 w-[5em]">Закрыто</p>
                            </div>
                        </div>
                    </div>
                </div>)}
            </div>
        </div>
    );
};