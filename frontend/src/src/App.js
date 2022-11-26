import React from 'react';

import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';

import Navbar from './containers/Navbar';
import Main from './pages/Main';
import Index from './pages/Index';
import CreateTask from './pages/CreateTask';
import Settings from './pages/Settings';
import Team from './pages/Team';
import About from './pages/About';
import Profile from './pages/Profile';
import CreateTeam from './pages/CreateTeam.js';
import Confirm from './pages/Confirm';
import JoinTeam from './pages/JoinTeam';
import TeamSettings from './pages/TeamSettings';
import Permission from './pages/Permission';
import ChangeUsername from './pages/ChangeUsername';
import ChangePassword from './pages/ChangePassword';
import store from './features/store';
import { Provider } from 'react-redux';


export default function App() {
  return (
    <Provider store={store}>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Index />}></Route>
          <Route path="/main" element={<Main />}></Route>
          <Route path="/create_task" element={<CreateTask />}></Route>
          <Route path="/create_team" element={<CreateTeam />}></Route>
          <Route path="/settings" element={<Settings />}></Route>
          <Route path="/team" element={<Team />}></Route>
          <Route path="/about" element={<About />}></Route>
          <Route path="/profile" element={<Profile />}></Route>
          <Route path="/confirm" element={<Confirm />}></Route>
          <Route path="/join" element={<JoinTeam />}></Route>
          <Route path="/team_settings" element={<TeamSettings />}></Route>
          <Route path="/permission" element={<Permission />}></Route>
          <Route path="/change_username" element={<ChangeUsername />}></Route>
          <Route path="/change_password" element={<ChangePassword />}></Route>
        </Routes>
      </Router>
    </Provider>
  );
};
