const isAuthenticate = () => {
  // return false
  if (localStorage.getItem('userName') === null) return false
  else return true
}

const isCreator = () => {
  if (localStorage.getItem('identity') === 'creator') return true
  else return false
}
export { isAuthenticate, isCreator }
