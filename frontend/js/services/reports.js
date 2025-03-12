import { API_URL } from '../config/config.js';

export async function fetchTotalItems(endpoint) {
  const response = await fetch(`${API_URL}/${endpoint}`);
  const data = await response.json();
  return data[0]?.total || data.length;
}

export async function fetchData(endpoint, page, paginationLimit) {
  const response = await fetch(`${API_URL}/${endpoint}?page=${page}&per_page=${paginationLimit}`);
  const items = await response.json();
  return items;
}
