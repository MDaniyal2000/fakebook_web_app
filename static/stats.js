import { CountUp } from './countUp.min.js';

window.onload = function() {
    let all_users = new CountUp(document.getElementById('allUsers'), 104983);
    if (!all_users.error) {
      all_users.start();
    } else {
      console.error(all_users.error);
    }

    let new_users = new CountUp(document.getElementById('newUsers'), 9815);
    if (!new_users.error) {
      new_users.start();
    } else {
      console.error(new_users.error);
    }

    let online_since = new CountUp(document.getElementById('onlineSince'), 2020);
    if (!online_since.error) {
      online_since.start();
    } else {
      console.error(online_since.error);
    }
}