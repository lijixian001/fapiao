import request from '@/utils/request'

export function getInvoiceList(params) {
  return request({
    url: '/invoice',
    method: 'get',
    params
  })
}

export function getInvoiceDetail(id) {
  return request({
    url: `/invoice/${id}`,
    method: 'get'
  })
}

export function createInvoice(data) {
  return request({
    url: '/invoice',
    method: 'post',
    data
  })
}

export function updateInvoice(id, data) {
  return request({
    url: `/invoice/${id}`,
    method: 'put',
    data
  })
}

export function deleteInvoice(id) {
  return request({
    url: `/invoice/${id}`,
    method: 'delete'
  })
}

export function archiveInvoice(id) {
  return request({
    url: `/invoice/${id}/archive`,
    method: 'post'
  })
}

export function unarchiveInvoice(invoice_id) {
  return request({
    url: '/invoice/archive/unarchive',
    method: 'post',
    params: { invoice_id }
  })
}

export function verifyInvoice(id) {
  return request({
    url: `/invoice/${id}/verify`,
    method: 'post'
  })
}
