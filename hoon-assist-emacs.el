(require 'json)

(defun xah-print-hash (hashtable)
  "Prints the hashtable, each line is key, val"
  (maphash
   (lambda (k v)
     (insert "this is the key:  ")
     (insert (format "%s" k))
     (insert "\n")
     (insert "this is the val:  ")
     (insert "<html><body>")
     (insert (format "%s" v))
     (insert "</body></html>"))
   hashtable
   ))

(defun prep-foo-buffer ()
  (progn
   (if (get-buffer "foo")(kill-buffer "foo"))
   (generate-new-buffer "foo")
   (with-current-buffer "foo" (html-mode))
   (with-current-buffer "foo" (goto-char 0))
   (with-current-buffer "foo" (insert "json is next3\n"))
   ))

(defun get-rune-desc ()
  (let* ((json-object-type 'hash-table)
	 (json-array-type 'list)
	 (json-key-type 'string)
	 (json (json-read-file "/home/mbc/projects/hoon-assist-emacs/hoon-dictionary.json"))
	 (first (caar json))
	 (dummy (prep-foo-buffer))
	 )
;;    (gethash rune json)
;; (with-current-buffer "foo"  (insert  (format "%s"  first)))
 (with-current-buffer "foo"  (xah-print-hash  (car json)))
    ))

;;(generate-new-buffer "foo")
;;(with-current-buffer "foo" (erase-buffer))
;;(with-current-buffer "foo" (html-mode))
 ;;(with-current-buffer "foo" ; replace with the name of the buffer you want to append
 ;   (goto-char 0)
    (get-rune-desc  )
;;  (insert  (json-read-file "/home/mbc/projects/hoon-assist-emacs/hoon-dictionary.json")))
 
















(defun my-json-string-valid-p (string)
  "Validates a JSON string."
  (condition-case nil
      (progn
        (json-read-from-string string)
        t)
    (error nil)))
